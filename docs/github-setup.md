# Configuração do GitHub

## Estado verificado — 06/10/2026

[Repositório CTA Financeiro](https://github.com/luismschiazza/cta-financeiro), com branch padrão `main` e Issues habilitadas. O dono tornou o repositório **público** para disponibilizar o código; essa decisão substitui a premissa privada do pacote inicial. O [Project CTA Financeiro — Kanban](https://github.com/users/luismschiazza/projects/1/views/1) é **privado**. As issues do repositório continuam públicas.

As 23 tarefas foram publicadas como issues #1–#23, na ordem de `planning/issues.json`, com critérios de aceite, validação e referências às dependências reais. F01 é [#1](https://github.com/luismschiazza/cta-financeiro/issues/1); a próxima é F02 [#2](https://github.com/luismschiazza/cta-financeiro/issues/2).

## CI executada

- Commit inicial: `eb9b09c03e1a3fff7f2cf530826a0f40ec48b94f`.
- [Execução da Fundação #37384950012](https://github.com/luismschiazza/cta-financeiro/actions/runs/37384950012): **success**, com job `foundation` aprovado.
- Dependabot para GitHub Actions configurado e execução inicial aprovada. npm será incluído quando existirem manifests e lockfiles.
- A CI atual valida estrutura, documentação, planejamento, ações por SHA e título convencional do PR. Lint TypeScript, build, testes da API, banco, migrations e segurança completa serão implementados em F02–F06.

## Proteções aplicadas

Ruleset **main — PR e CI obrigatórios**, ID `24547545`, ativo na branch padrão, sem bypass configurado.

| Regra | Configuração verificada |
| --- | --- |
| Entrada na main | Pull request obrigatório |
| Check obrigatório | `foundation`, originado de GitHub Actions |
| Atualização da branch | Obrigatória antes do merge |
| Merge | Somente squash; merge commit e rebase desabilitados |
| Histórico | Linear |
| Conversas de revisão | Resolução obrigatória |
| Force push e exclusão | Bloqueados |
| Aprovações independentes | 0: existe apenas o dono; ele não pode aprovar o próprio PR |
| Bypass | Nenhum |

CODEOWNERS identifica o responsável, mas não representa revisão independente. Quando houver outro revisor, reavaliar a exigência de aprovação. A configuração foi conferida tanto na interface quanto pela leitura do ruleset pela API.

## GitHub Actions e fechamento de tarefas

- `GITHUB_TOKEN` com leitura de contents/packages por padrão; criação/aprovação de PR por workflows desabilitada. O workflow Fundação limita sua permissão a `contents: read` e checkout sem persistir credenciais.
- Actions devem estar fixadas em SHA completo de commit; política do repositório habilitada.
- Execuções de PRs de todos os colaboradores externos exigem aprovação.
- Fechamento automático de issues por merge desabilitado. Conferir critérios e evidências antes de fechar a issue; fechamento move o cartão para Concluído.
- No Project, automações de concluir por merge e avançar ao vincular PR estão desabilitadas. Status, campos e limites estão descritos em [Kanban](kanban.md).

## Ambientes e próximos checks

Dev, staging e prod serão provisionados em F09/F10. Cada um terá secrets e recursos próprios; `test` é descartável e `local` não é ambiente remoto. Aprovação de prod deve usar o mecanismo suportado ou um processo manual verificável. Ainda não há infraestrutura de deploy ou execução de migrations remotas.

Quando F06 entregar os checks completos, acrescentá-los às regras da main após verificar execuções reais. Não exigir jobs ainda ausentes. Reavaliar a disponibilidade de proteções se a visibilidade ou o plano do GitHub mudar.

## Evidência de conclusão de F01

A [issue #1](https://github.com/luismschiazza/cta-financeiro/issues/1) concentra a evidência final do PR, SHA integrado e CI. Fechar somente após integrar a atualização documental com check aprovado e conferir o quadro. Os critérios de criação privada foram ajustados à decisão explícita do dono de manter o repositório público.

[GitHub Environments e disponibilidade](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)
