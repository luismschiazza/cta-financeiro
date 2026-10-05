#!/usr/bin/env python3
"""Checks iniciais da fundação; não executa testes da aplicação financeira."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from render_kanban import render as render_kanban

ROOT = Path(__file__).resolve().parents[1]
TITLE = re.compile(r'^(feat|fix|docs|test|chore|ci|refactor|perf|build|revert)(\([a-zA-Z0-9_./-]+\))?!?: \S.+$')


def check_pr_title():
    if not TITLE.fullmatch(os.environ.get('PR_TITLE', '')):
        print('Título inválido: use tipo(escopo opcional): descrição.', file=sys.stderr)
        return 1
    print('Título do PR aprovado.')
    return 0


def check():
    errors = []
    required = [
        'README.md', 'CONTRIBUTING.md', 'SECURITY.md', 'CHANGELOG.md', 'VERSION',
        '.gitignore', '.env.example', '.github/CODEOWNERS',
        '.github/workflows/foundation.yml', '.github/dependabot.yml',
        '.github/ISSUE_TEMPLATE/tarefa.yml', '.github/ISSUE_TEMPLATE/bug.yml',
        '.github/pull_request_template.md', 'planning/issues.json',
        'docs/arquitetura.md', 'docs/ambientes.md', 'docs/migrations.md',
        'docs/ci-cd.md', 'docs/validacao.md', 'docs/recuperacao.md',
        'docs/github-setup.md', 'docs/backlog.md', 'docs/kanban.md',
        'planning/kanban.json', 'planning/kanban.html', 'scripts/render_kanban.py',
    ]
    for name in required:
        if not (ROOT / name).is_file():
            errors.append(f'Arquivo obrigatório ausente: {name}')
    result = subprocess.run(['git', 'ls-files', '-z'], cwd=ROOT, capture_output=True, check=False)
    if result.returncode:
        print('Execute dentro de um repositório Git com arquivos adicionados ao índice.', file=sys.stderr)
        return 1
    tracked = [p for p in result.stdout.decode().split('\0') if p]
    if not tracked:
        errors.append('Nenhum arquivo versionado. Adicione os arquivos ao índice antes do check.')
    for name in required:
        if name not in tracked:
            errors.append(f'Arquivo obrigatório não versionado: {name}')

    secrets = [
        re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
        re.compile(r'\bgh[pousr]_[A-Za-z0-9]{30,}\b'),
        re.compile(r'\bgithub_pat_[A-Za-z0-9_]{40,}\b'),
    ]
    text_suffixes = {'.md', '.py', '.json', '.yml', '.yaml', '.sql', '.ts', '.js', '.mjs', '.sh', '.ps1'}
    for name in tracked:
        p = Path(name)
        if (p.name == '.env' or p.name.startswith('.env.')) and p.name != '.env.example':
            errors.append(f'Configuração privada versionada: {name}')
        if p.suffix.lower() in {'.dump', '.backup', '.ofx', '.dbf', '.dbt', '.pem', '.key', '.p12', '.pfx'}:
            errors.append(f'Arquivo privado/bancário proibido: {name}')
        if any(part in {'backups', 'imports', 'exports', 'data'} for part in p.parts):
            errors.append(f'Pasta de dados privados versionada: {name}')
        path = ROOT / name
        if not path.is_file():
            errors.append(f'Arquivo versionado ausente: {name}')
            continue
        if path.stat().st_size > 2_000_000:
            errors.append(f'Arquivo grande exige revisão fora deste pacote: {name}')
            continue
        if p.suffix not in text_suffixes and p.name not in {'VERSION', '.env.example', '.gitignore', '.editorconfig', '.gitattributes', 'CODEOWNERS'}:
            continue
        try:
            content = path.read_text(encoding='utf-8')
        except UnicodeError:
            errors.append(f'Texto não está em UTF-8: {name}')
            continue
        if content and not content.endswith('\n'):
            errors.append(f'Falta quebra final: {name}')
        if any(line.rstrip(' \t') != line for line in content.splitlines()):
            errors.append(f'Espaço no fim da linha: {name}')
        if any(pattern.search(content) for pattern in secrets):
            errors.append(f'Possível secret versionado: {name}')
        if p.suffix == '.md':
            for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', content):
                if target.startswith(('#', 'http:', 'https:', 'mailto:')):
                    continue
                destination = target.split('#', 1)[0]
                if destination and not (path.parent / destination).exists():
                    errors.append(f'Link local quebrado em {name}: {target}')
        if name.startswith('.github/workflows/'):
            for action in re.findall(r'uses:\s*([^\s#]+)', content):
                if action.startswith('./'):
                    continue
                if not re.fullmatch(r'[^@]+@[0-9a-f]{40}', action):
                    errors.append(f'Action sem SHA completo: {name}')
            if 'pull_request_target:' in content:
                errors.append(f'Gatilho privilegiado exige revisão separada: {name}')

    try:
        version = (ROOT / 'VERSION').read_text().strip()
        if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?', version):
            errors.append('VERSION deve usar SemVer.')
        env_lines = (ROOT / '.env.example').read_text().splitlines()
        env = {}
        for line in env_lines:
            if line.strip() and not line.lstrip().startswith('#'):
                key, value = line.split('=', 1)
                if key in env:
                    errors.append(f'Variável duplicada no exemplo: {key}')
                env[key] = value
        expected = {'APP_ENV', 'NODE_ENV', 'DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_TLS_MODE', 'MIGRATION_DB_USER', 'MIGRATION_DB_PASSWORD', 'BANK_INTEGRATION_MODE', 'PAYMENTS_ENABLED'}
        for key in sorted(expected - env.keys()):
            errors.append(f'Contrato de configuração incompleto: {key}')
        if env.get('APP_ENV') != 'local' or env.get('BANK_INTEGRATION_MODE') != 'mock' or env.get('PAYMENTS_ENABLED') != 'false':
            errors.append('Exemplo deve usar local, mock e pagamentos desabilitados.')
        if env.get('DB_PASSWORD') or env.get('MIGRATION_DB_PASSWORD'):
            errors.append('Exemplo não deve conter senhas preenchidas.')
        issues = json.loads((ROOT / 'planning/issues.json').read_text())
        board = json.loads((ROOT / 'planning/kanban.json').read_text())
        columns = {column['name']: column['wip_limit'] for column in board['columns']}
        if list(columns) != ['Backlog', 'A fazer', 'Em andamento', 'Em revisão', 'Concluído']:
            errors.append('Colunas Kanban inválidas.')
        if columns.get('A fazer') != 3 or columns.get('Em andamento') != 1 or columns.get('Em revisão') != 1 or board['active_wip_limit'] != 2:
            errors.append('Limites WIP diferentes da política documentada.')
        counts = {name: 0 for name in columns}
        by_id = {issue['id']: issue for issue in issues}
        orders = set()
        known = set()
        for issue in issues:
            key = issue['id']
            state = issue['status']
            if state not in columns:
                errors.append(f'Status Kanban inválido: {key}')
            else:
                counts[state] += 1
            if issue['priority'] not in board['priorities']:
                errors.append(f'Prioridade inválida: {key}')
            if not isinstance(issue['order'], int) or issue['order'] < 1 or issue['order'] in orders:
                errors.append(f'Ordem Kanban inválida: {key}')
            orders.add(issue['order'])
            if not isinstance(issue['blocked'], bool):
                errors.append(f'Marcador de bloqueio inválido: {key}')
            if issue['blocked'] and not issue['block_reason'].strip():
                errors.append(f'Bloqueio sem motivo: {key}')
            if issue['blocked'] and state == 'Concluído':
                errors.append(f'Tarefa bloqueada não pode estar concluída: {key}')
            if state in {'Em andamento', 'Em revisão', 'Concluído'}:
                if any(by_id.get(dep, {}).get('status') != 'Concluído' for dep in issue['dependencies']):
                    errors.append(f'Tarefa avançou com dependência pendente: {key}')
            if key in known:
                errors.append(f'ID repetido: {key}')
            for dependency in issue['dependencies']:
                if dependency not in known:
                    errors.append(f'Dependência ausente ou fora de ordem em {key}: {dependency}')
            if '## Critérios de aceite' not in issue['body'] or '- [ ] ' not in issue['body']:
                errors.append(f'Issue sem critérios verificáveis: {key}')
            known.add(key)
        for name, limit in columns.items():
            if limit is not None and counts[name] > limit:
                errors.append(f'Limite WIP excedido: {name}')
        if counts.get('Em andamento', 0) + counts.get('Em revisão', 0) > board['active_wip_limit']:
            errors.append('Limite global de trabalho ativo excedido.')
        if (ROOT / 'planning/kanban.html').read_text() != render_kanban():
            errors.append('Quadro visual desatualizado: execute scripts/render_kanban.py.')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f'Contrato da fundação inválido: {type(exc).__name__}')

    if errors:
        for error in errors:
            print(f'ERRO: {error}', file=sys.stderr)
        return 1
    print(f'Fundação aprovada: {len(tracked)} arquivos, {len(issues)} issues e links locais verificados.')
    print('Escopo: estrutura e contratos. Testes financeiros, migrations e deploy ainda não existem.')
    return 0


if __name__ == '__main__':
    sys.exit(check_pr_title() if '--pr-title' in sys.argv else check())
