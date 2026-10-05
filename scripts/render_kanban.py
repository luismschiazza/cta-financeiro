#!/usr/bin/env python3
"""Renderiza um snapshot local do Kanban, sem dependências ou sincronização remota."""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def render():
    issues = json.loads((ROOT / 'planning/issues.json').read_text())
    config = json.loads((ROOT / 'planning/kanban.json').read_text())
    parts = ['''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CTA Financeiro — Kanban</title>
<style>
:root { color-scheme:light dark; --bg:light-dark(#f4f5f7,#111820); --fg:light-dark(#17212b,#eef3f7); --surface:light-dark(#fff,#1c2732); --line:light-dark(#ccd4dc,#43505e); --muted:light-dark(#445363,#bac7d4); --flag:light-dark(#7d3800,#ffba78); }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--fg); font:16px/1.5 system-ui,sans-serif; }
main { max-width:1600px; margin:auto; padding:24px; }
h1 { margin:0 0 8px; font-size:28px; }
h2 { font-size:18px; margin:0 0 4px; }
p { margin:8px 0; }
a { color:inherit; }
.caption { color:var(--muted); }
.board { display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:16px; align-items:start; margin:24px 0; }
.column { min-width:0; }
.column > header { padding-bottom:12px; border-bottom:2px solid var(--line); margin-bottom:12px; }
.card { padding:14px; border:1px solid var(--line); border-radius:8px; background:var(--surface); margin:0 0 12px; overflow-wrap:anywhere; }
summary { cursor:pointer; font-weight:600; }
.meta { color:var(--muted); font-size:14px; }
.block { color:var(--flag); font-size:14px; }
.card section { margin-top:12px; }
ul { padding-left:20px; margin:8px 0; }
li { margin:6px 0; }
.empty { color:var(--muted); }
.legend { display:flex; flex-wrap:wrap; gap:8px 24px; padding:12px 0; }
footer { border-top:1px solid var(--line); padding-top:16px; }
@media(max-width:1150px) { .board { grid-template-columns:repeat(3,minmax(0,1fr)); } }
@media(max-width:760px) { .board { grid-template-columns:repeat(2,minmax(0,1fr)); } main { padding:16px; } }
@media(max-width:490px) { .board { grid-template-columns:1fr; } }
@media print { body { background:#fff; color:#000; } .board { display:block; } .card { break-inside:avoid; } }
</style>
</head>
<body>
<main>
<h1>CTA Financeiro — Kanban</h1>
<p>Fundação → Backend e banco → Frontend</p>
<p class="caption">Retrato inicial do planejamento · 23 tarefas · GitHub ainda não publicado</p>
<p><a href="../docs/kanban.md">Regras do fluxo</a> · <a href="../docs/backlog.md">Critérios completos</a></p>
<div class="legend" aria-label="Prioridades"><span>P0 · Fundação</span><span>P1 · MVP</span><span>P2 · Integração opcional</span><span>P3 · Descoberta futura</span></div>
<div class="board" aria-label="Quadro Kanban">
''']
    for column in config['columns']:
        name = column['name']
        cards = sorted((i for i in issues if i['status'] == name), key=lambda i: (i['priority'], i['order']))
        cap = column['wip_limit']
        limit = 'Sem limite' if cap is None else f'Limite {cap}'
        parts.append(f'<section class="column" aria-label="{escape(name)}"><header><h2>{escape(name)} · {len(cards)}</h2><span class="meta">{limit}</span></header>')
        if not cards:
            parts.append('<p class="empty">Nenhuma tarefa.</p>')
        for i in cards:
            objective = i['body'].split('## Objetivo\n\n', 1)[1].split('\n\n## Dependências', 1)[0]
            criteria = i['body'].split('## Critérios de aceite\n\n', 1)[1].split('\n\n## Validação', 1)[0]
            validation = i['body'].split('## Validação\n\n', 1)[1].strip()
            deps = ', '.join(i['dependencies']) or 'Nenhuma'
            parts.append(f'<article class="card" data-issue="{escape(i["id"])}" data-status="{escape(name)}">')
            parts.append(f'<p class="meta">{escape(i["priority"])} · {escape(i["phase"])}</p>')
            parts.append(f'<details><summary>{escape(i["title"])}</summary>')
            parts.append(f'<section><p>{escape(objective)}</p><p><strong>Dependências:</strong> {escape(deps)}</p><strong>Critérios de aceite</strong><ul>')
            for line in criteria.splitlines():
                if line.startswith('- [ ] '):
                    parts.append(f'<li>{escape(line[6:])}</li>')
            parts.append(f'</ul><p><strong>Validação:</strong> {escape(validation)}</p></section></details>')
            if i['blocked']:
                parts.append(f'<p class="block"><strong>Bloqueada:</strong> {escape(i["block_reason"])}</p>')
            parts.append('</article>')
        parts.append('</section>')
    parts.append('''</div>
<footer>
<p><strong>Limites:</strong> 1 tarefa em andamento e 1 em revisão; máximo de 2 no trabalho ativo.</p>
<p>Concluir exige critérios atendidos, validação registrada e mudança integrada. Bloqueio conserva a coluna e exige motivo.</p>
<p class="caption">Quadro de consulta gerado dos dados versionados. Abra os cartões para ver o aceite. Alterações de estado são feitas em issues.json; este arquivo não altera o GitHub.</p>
</footer>
</main>
</body>
</html>
''')
    return '\n'.join(parts)


if __name__ == '__main__':
    path = ROOT / 'planning/kanban.html'
    path.write_text(render(), encoding='utf-8')
    print('Quadro Kanban atualizado: planning/kanban.html')
