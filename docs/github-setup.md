# Configuração do GitHub

## Estado

Pacote preparado em 05/10/2026 para `luismschiazza/cta-financeiro`. O repositório privado ainda não foi criado. Nome/owner deverão ser conferidos na criação. Não há proteções, environments, secrets, issues ou Actions remotos configurados pelo pacote.

## F01: aplicar e verificar

- Criar repositório **Private** com nome `cta-financeiro`, descrição do README e branch `main`.
- Subir os arquivos com commit `chore: preparar fundação do CTA financeiro`.
- Confirmar visibilidade privada, habilitação de Issues e execução do workflow.
- Habilitar squash merge; bloquear force push e exclusão de `main` pelas regras disponíveis.
- Exigir PR e resolução de conversas; configurar `foundation` como check obrigatório após a primeira execução bem-sucedida.
- Aplicar checks completos quando F06 existir; não exigir jobs ainda ausentes.
- Definir política de revisão compatível com equipe real. CODEOWNERS aponta para o dono e não substitui aprovação independente.
- Token de Actions com leitura por padrão; evitar permissão global de escrita e aprovação automática de PRs.
- Ativar Dependabot para Actions; incluir npm quando manifests/lockfiles existirem.
- Verificar recursos de proteção/environments do plano contratado. Se indisponíveis, registrar limitação e solução; não declarar enforcement inexistente.
- Abrir issues de `planning/issues.json` na ordem do backlog e ligar dependências aos números reais.
- Criar Project privado em Board conforme [Kanban](kanban.md), usando as mesmas issues, campos e estados; verificar acesso e limites disponíveis.

## Environments futuros

Dev, staging e prod são provisionados em F09/F10. Cada um tem secrets e recursos próprios; `test` é descartável e `local` não é ambiente remoto. Aprovação de prod deve ser garantida pelo mecanismo suportado ou processo manual verificável. Sem infraestrutura definida, não adicionar workflow de deploy aparentemente funcional.

## Verificação de conclusão

Registrar URL do repositório, SHA do commit, URL e resultado da CI, números das issues e evidência das proteções aplicadas. Recursos pendentes devem continuar abertos no backlog.

[GitHub Environments e disponibilidade](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)
