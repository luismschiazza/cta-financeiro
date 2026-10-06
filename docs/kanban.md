# Kanban do CTA Financeiro

## Quadro

[Abra o quadro visual](../planning/kanban.html). A fonte dos cartões é `planning/issues.json`; colunas e limites estão em `planning/kanban.json`. A visualização é um retrato do planejamento, sem sincronização com GitHub ou alteração automática dos estados.

| Coluna | Significado | Limite de tarefas |
| --- | --- | --- |
| Backlog | Planejada; ainda não selecionada ou com dependências pendentes | Sem limite |
| A fazer | Selecionada como próxima; explicitar qualquer bloqueio | 3 |
| Em andamento | Implementação iniciada e sem impedimento para executar | 1 |
| Em revisão | Implementação pronta; conferir PR, critérios e checks | 1 |
| Concluído | Critérios atendidos, validação registrada e mudança integrada | Sem limite |

No máximo duas tarefas somando Em andamento e Em revisão. Isso evita iniciar várias mudanças antes de terminar a anterior. Limites são tetos, não metas.

## Regras de movimentação

1. Puxar tarefas por prioridade e dependências: fundação -> backend e banco -> frontend. Integração bancária por API é opcional para o MVP; extrato permanece um caminho válido.
2. Para A fazer: objetivo claro, critérios de aceite, validação prevista e dependências verificadas. Uma pendência externa pode manter o cartão nessa fila, mas deve ter marcador de bloqueio e motivo.
3. Para Em andamento: dependências concluídas, acesso necessário disponível e limite livre. Trabalhar em uma branch por tarefa; evitar agentes editando a mesma branch simultaneamente.
4. Para Em revisão: PR ou mudança revisável pronta, checks aplicáveis passando e evidência dos critérios. Migrations e dinheiro exigem validação específica.
5. Para Concluído: critérios confirmados, CI aplicável aprovada, mudança integrada e documentação atualizada. Tarefa de publicação também exige evidência da execução no GitHub/ambiente; Markdown pronto não comprova infraestrutura ativa.
6. Se a revisão encontrar falha, voltar para Em andamento respeitando o limite. Bloqueio nunca conta como conclusão.

Bloqueado é um marcador com motivo, não uma sexta coluna. O cartão conserva sua posição e conta no limite da coluna. Não abrir trabalho extra para esconder um bloqueio; resolver, dividir ou devolver ao Backlog de forma explícita.

## Prioridades

| Prioridade | Uso |
| --- | --- |
| P0 | Base obrigatória: ambientes, migrations, CI/CD, segurança e recuperação |
| P1 | Entrega financeira e frontend do MVP |
| P2 | Integração bancária opcional |
| P3 | Bot da prefeitura e pagamentos: descoberta futura |

## Estado após F01 — 06/10/2026

[Project privado CTA Financeiro — Kanban](https://github.com/users/luismschiazza/projects/1/views/1), ligado às mesmas 23 issues do repositório. F01 concluída, F02 em A fazer e as outras 21 no Backlog, após integrar e validar a entrega de F01. O bloqueio anterior de publicação foi resolvido. A próxima tarefa é F02, para iniciar o NestJS; as tarefas Angular continuam após B05.

O quadro usa Status com as cinco colunas acima, Priority (P0–P3), Phase, Order (1–23) e Blocked (Sim/Não). A ordenação é Priority e depois Order. Os limites 3/1/1 estão configurados nas colunas; o limite total de duas tarefas ativas permanece uma política conferida antes de cada movimentação. Os números do GitHub correspondem à ordem: F01 #1, F02 #2, ..., X02 #23.

## Operação do GitHub Project

As issues reais contêm referências às dependências pelos números do GitHub. Não criar issues duplicadas para representar cartões. O check local valida os limites e estados do snapshot versionado; não altera o Project remoto. Conferir ambos quando atualizar o retrato.

Não marcar Concluído apenas por criação ou merge de PR. As automações do Project que concluíam por merge ou avançavam ao vincular PR foram desabilitadas; o fechamento automático de issues por merge também está desabilitado. Depois de verificar aceite, CI e integração, fechar a issue: a automação de issue fechada move o cartão para Concluído. Novos itens entram no Backlog.

## Atualizar o retrato do quadro

Editar os estados/prioridades em `planning/issues.json`, respeitando as regras. Depois executar:

```bash
python3 scripts/render_kanban.py
python3 scripts/check_foundation.py
```

No Windows, usar `py -3` no lugar de `python3`. O render gera novamente `planning/kanban.html` a partir dos dados versionados.
