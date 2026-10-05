# Contribuição e versionamento

## Fluxo

Usar o [Kanban](docs/kanban.md), respeitando dependências e limite de uma tarefa Em andamento e uma Em revisão. Concluir exige evidência dos critérios, não apenas mudar o cartão.

Uma issue por objetivo pequeno e verificável. Abrir branch a partir de `main`: `feat/B01-contas`, `fix/B03-duplicidade`, `chore/F03-config` ou `docs/F01-readme`. Branches não representam ambientes.

PR informa problema, mudança, issue relacionada, validação e risco. Usar squash merge com título convencional. Evitar edições simultâneas de agentes na mesma branch. Não misturar funcionalidades sem dependência.

## Commits

Usar Conventional Commits: `feat`, `fix`, `docs`, `test`, `chore`, `ci`, `refactor`, `perf`, `build` ou `revert`. Escopo opcional e mudança incompatível com `!` e descrição no corpo. Exemplos: `ci: validar migrations no PostgreSQL`, `feat(contas): cadastrar conta bancária`.

## Versões

`VERSION` começa em `0.1.0`, ainda não publicado. Registrar mudanças em `CHANGELOG.md` em Unreleased. Releases seguem SemVer e tags `vX.Y.Z` após validação. Nenhuma tag será criada neste pacote.

A versão da aplicação, o commit/digest e as migrations aplicadas são rastreados separadamente. Não renomear migration porque a versão da aplicação mudou. Quando houver packages, manter versões conforme a estratégia fixada na F02.

## Dependências

Versões exatas, lockfile e versão do runtime versionados. Instalação reproduzível com `npm ci`. Atualizações por PR com validação; evitar `latest` em Docker, Actions ou manifests de produção.

## Pronto para merge

- Critérios da issue atendidos e evidência registrada.
- Checks aplicáveis passam; testes verificam comportamento e casos de falha.
- Mudança de banco tem migration, teste de instalação/upgrade e plano operacional.
- Secrets, dados reais e dumps estão fora do Git.
- Configuração e documentação atualizadas.
- Alteração financeira ou de acesso inclui cenários de permissão, concorrência e precisão quando aplicáveis.

Configuração de proteção de `main` depende das regras reais no GitHub. Revisão independente é preferível para mudanças financeiras e deploy de produção; CODEOWNERS sozinho não impede merge e o autor não pode aprovar o próprio PR.
