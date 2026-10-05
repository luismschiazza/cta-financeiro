# CI/CD

## O que existe neste pacote

Workflow `Fundação` em PRs, pushes em `main` e execução manual. Token com `contents: read`, checkout fixado por SHA e sem persistir credenciais. Executa `check_foundation.py` e verifica título convencional do PR. Dependabot acompanha GitHub Actions semanalmente.

Esse workflow não executa aplicação ou deploy. O check chama-se `foundation`; não registrá-lo como prova de testes financeiros.

## CI completa a implementar em F06

| Check | Critério para passar |
| --- | --- |
| foundation | Estrutura, contratos, exemplos e arquivos permitidos |
| lint | ESLint e formatação do código sem erros |
| typecheck | TypeScript estrito sem erros |
| unit | Regras financeiras e autorização testadas |
| integration | API/persistência com PostgreSQL descartável |
| migrations | Instalação vazia, upgrade e histórico preservado |
| build | Backend e, quando existir, frontend compilados |
| security | Segredos, dependências e workflows analisados |
| required-checks | Todos os checks esperados concluídos com sucesso |

Usar `npm ci` com lockfile e versões fixadas. Testes vazios, scripts `echo`, `passWithNoTests` e `continue-on-error` não satisfazem os gates. Não usar filtros por caminho que deixem checks obrigatórios eternamente pendentes. O agregador roda sempre e falha se um check necessário for omitido, cancelado ou falhar.

Vulnerabilidades altas/críticas relevantes bloqueiam merge; exceções precisam de justificativa, responsável e vencimento no repositório. Nenhum scan oferece garantia de ausência de falhas. Fixar Actions por SHA e atualizar por PR. PR não recebe credenciais de produção. Evitar `pull_request_target` para executar código contribuído.

## CD a implementar em F09/F10

1. Após CI aprovada no commit de `main`, construir artefato imutável uma vez e registrar SHA, digest, versão e conjunto de migrations.
2. Publicar em dev com credenciais de dev e executar smoke tests.
3. Promover o mesmo digest para staging, aplicar migrations em job serializado e testar o fluxo financeiro.
4. Produção só aceita versão aprovada em staging e liberação humana explícita. Tag sozinha não autoriza deploy.
5. Aplicar migrations compatíveis, publicar o mesmo artefato e conferir saúde, versão, conectividade e smoke tests sem mutar dinheiro real.
6. Falha interrompe promoção. Rollback de aplicação usa artefato anterior; banco segue procedimento específico compatível.

Deploys concorrentes no mesmo ambiente são serializados. Não cancelar migration já iniciada. Não reconstruir artefatos entre staging e prod. Registrar resultado, executor e evidências de cada promoção.

## Dependências externas ainda abertas

Escolher hospedagem, registry, backups e gestão de secrets; definir orçamento. GitHub Environments e proteções dependem do plano e tipo de repositório. Se uma trava não estiver disponível, documentar bloqueio e escolher alternativa verificável. Não registrar proteção como ativa só porque está no Markdown.

## Referências verificadas em 05/10/2026

- [Segurança no GitHub Actions](https://docs.github.com/en/actions/reference/security/secure-use)
- [Gestão de environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)
- [Release de checkout usada](https://github.com/actions/checkout/releases/tag/v7.0.1)
