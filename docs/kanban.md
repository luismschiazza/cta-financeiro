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

## Estado inicial

23 cartões: 22 no Backlog e F01 em A fazer, com bloqueio de publicação no GitHub. Nenhum cartão está em andamento, revisão ou concluído. Os arquivos da fundação estão preparados; F01 continua pendente porque o repositório e suas proteções ainda não foram publicados.

A próxima tarefa é F01. Depois vem F02, para iniciar o NestJS. Cada issue financeira entrega backend, migration e testes juntos; as tarefas Angular continuam após B05.

## Aplicação futura no GitHub Projects

Criar Project privado com visualização Board e agrupamento por Status. Configurar as cinco opções acima; campos Priority (P0–P3), Phase, Order e Blocked. Ligar os cartões às issues reais do repositório, mantendo os IDs F/B/W/X e dependências nos corpos. Ordenar por Priority e Order. Não criar issues duplicadas para representar cartões.

Limites WIP são políticas da equipe; o quadro não garante seu bloqueio automaticamente. O check local valida limites e estados do snapshot versionado. Na operação do Project, revisar limites antes de mover cartões e manter o snapshot atualizado quando ele for usado como registro.

Evitar automação que marque concluído apenas por criação ou merge de PR: conferir também aceite e evidências. A criação do Project e das issues reais ainda está pendente de acesso ao GitHub.

## Atualizar o retrato do quadro

Editar os estados/prioridades em `planning/issues.json`, respeitando as regras. Depois executar:

```bash
python3 scripts/render_kanban.py
python3 scripts/check_foundation.py
```

No Windows, usar `py -3` no lugar de `python3`. O render gera novamente `planning/kanban.html` a partir dos dados versionados.
