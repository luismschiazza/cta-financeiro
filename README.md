# CTA Financeiro

Sistema financeiro para a clínica CTA, com conferência de movimentações bancárias, conciliação, receitas, despesas e relatórios mensais.

**Situação:** fundação e planejamento. Este pacote contém documentação, modelos do GitHub e uma CI de estrutura. Ainda não contém aplicação NestJS/Angular, migrations executáveis, integrações reais nem deploy. O repositório remoto e suas proteções precisam ser configurados.

## Objetivo da primeira entrega

Importar dados de forma rastreável, impedir duplicidades, conferir saldos e apresentar relatórios consistentes. Desenvolver backend e banco juntos; construir o frontend depois que a API estiver validada.

## Escopo

- Contas bancárias, movimentações e categorias financeiras.
- Importações com lote, origem e resultado registrado.
- Conciliação, divergências e resumo mensal.
- Autenticação, permissões, auditoria e recuperação por backup.
- Consulta dos dados do legado após comparar registros e totais.

Pessoas serão cadastradas apenas quando necessárias para identificar pagamentos. Prontuários, evoluções clínicas, internações e vagas não fazem parte desta primeira entrega. API bancária, pagamentos automáticos e bot da prefeitura exigem descoberta própria; os dois últimos estão fora do MVP.

## Base técnica

| Parte | Escolha |
| --- | --- |
| Backend | NestJS e TypeScript com modo estrito |
| Banco | PostgreSQL com migrations versionadas |
| Frontend | Angular, iniciado depois da API |
| Testes | Jest; integração com PostgreSQL descartável; E2E |
| Dependências | npm, versões exatas e lockfile versionado |
| Estrutura | Monólito modular, um repositório |
| Entrega | GitHub Actions, artefatos identificados por commit/digest |

Node 24 LTS é a linha planejada. As versões exatas de runtime, frameworks, ORM e imagens serão verificadas e fixadas na issue F02. O ORM não foi escolhido neste pacote.

## Ambientes

| Ambiente | Finalidade | Dados |
| --- | --- | --- |
| local | Desenvolvimento na máquina | Fictícios, banco local |
| dev | Integração compartilhada | Fictícios, banco próprio |
| test | Testes automatizados | Banco descartável por execução |
| staging | Validar a entrega próxima de produção | Sintéticos ou anonimizados, banco próprio |
| prod | Operação autorizada | Dados reais, acesso restrito |

Cada ambiente tem bancos, usuários, credenciais e serviços separados. Branch não define ambiente. Nenhum teste automatizado pode acessar produção.

## Documentação

- [Arquitetura](docs/arquitetura.md)
- [Ambientes e configuração](docs/ambientes.md)
- [Migrations e banco](docs/migrations.md)
- [CI/CD e publicação](docs/ci-cd.md)
- [Validação financeira e testes](docs/validacao.md)
- [Backup e recuperação](docs/recuperacao.md)
- [Quadro e regras Kanban](docs/kanban.md)
- [Backlog ordenado](docs/backlog.md)
- [Configuração do GitHub](docs/github-setup.md)
- [Contribuição e versionamento](CONTRIBUTING.md)
- [Segurança](SECURITY.md)
- [Registro de mudanças](CHANGELOG.md)

## Verificar esta fundação

Git e Python 3.12 ou superior são suficientes. Dentro da pasta, após iniciar o repositório e adicionar os arquivos ao índice:

```bash
python3 scripts/check_foundation.py
```

No Windows, use `py -3 scripts/check_foundation.py`. A CI faz essa mesma verificação e valida o título dos PRs. Ela verifica apenas a fundação: não substitui lint TypeScript, build, testes da API, validação de migrations ou varredura completa de segredos.

## Próxima execução

Aplicar as configurações de F01 no GitHub. Depois iniciar F02: estrutura mínima do backend, ferramentas e versões fixadas. As demais issues seguem o [Kanban](docs/kanban.md): Backlog, A fazer, Em andamento, Em revisão e Concluído, com uma tarefa em implementação por vez. Não conectar banco real ou executar pagamentos nesta etapa.

## Progresso anterior

No estudo local, foi criado `cta_financeiro_dev`, com `contas_bancarias` e `movimentacoes_bancarias`. A conta fictícia Bradesco PJ tem ID 1, com entrada de R$ 200,00 em 29/09/2026. Esse banco ainda não representa uma instalação reproduzível por migrations; sua adaptação está prevista em F05.

## Uso

Projeto privado. Não há licença aberta concedida por este repositório. Não versionar dados de pacientes, extratos reais, credenciais ou backups.
