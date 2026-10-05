# Validação e testes

## Regras financeiras

| Regra | Backend | Banco | Teste mínimo |
| --- | --- | --- | --- |
| Valor positivo | Decimal válido, escala/limites definidos | NOT NULL e CHECK valor > 0 | Zero, negativo, precisão excedida |
| Tipo entrada/saída | Valor permitido no domínio | CHECK/enum escolhido | Tipo inválido |
| Conta existente | Verificar acesso e existência | FK obrigatória | Conta ausente e sem permissão |
| Identidade externa | Chave definida por origem | UNIQUE conta + ID externo, quando presente | Reimportação e concorrência |
| Lote de importação | Origem e resultado rastreáveis | FK e estados consistentes | Falha parcial, retomada |
| Dinheiro exato | Decimal/string, nunca soma com Number | NUMERIC com escala definida | Somatórios exatos e limites |
| Datas consistentes | Data bancária separada da importação | Tipos adequados | Virada de mês/fuso |
| Correções rastreáveis | Permissão e justificativa | Histórico/auditoria | Correção mantém evidência |

Nome do remetente auxilia conferência, mas não prova identidade. O identificador externo pode não existir em certos arquivos; a estratégia alternativa deve ser validada e nunca descartar transações legítimas automaticamente.

## Camadas

- DTO: tipos, formatos, limites, campos inesperados e mensagens compreensíveis.
- Domínio: regras financeiras aplicadas também a jobs e importações.
- Banco: constraints e transações contra erros e concorrência.
- Acesso: autenticação e autorização em cada operação sensível.
- Frontend futuro: ajuda na entrada; backend continua responsável pela validação.

Rejeitar entradas fora do contrato; não arredondar valores silenciosamente. Paginação e limites de arquivo/lote são obrigatórios para imports e consultas.

## Cenários de aceitação do MVP

1. Saldo inicial de R$ 1.000,00, entradas de R$ 200,00 e R$ 300,00, saída de R$ 150,00: saldo final R$ 1.350,00.
2. Reimportar o mesmo lote não altera contagem nem saldo.
3. Duas importações concorrentes da mesma transação produzem um registro.
4. Duas transações legítimas com mesma data e valor não são perdidas.
5. Falha de importação deixa resultado rastreável e permite retomar sem duplicar.
6. Usuário sem permissão não acessa ou altera os dados financeiros restritos.
7. Relatório mensal confere com o razão de movimentações e os totais da fonte.
8. Movimentação ainda não conciliada aparece pendente; divergência permanece visível.
9. Backup restaurado em ambiente isolado mantém contagens, totais e histórico.

Saldo, fluxo de caixa e lucro são conceitos diferentes. A primeira entrega apresenta entradas, saídas e saldo; lucro contábil só será apresentado se houver modelo e critérios suficientes.

## Estratégia

Testes unitários para regras; integração para constraints/transações; E2E para autenticação, importação e conciliação; smoke tests após deploy. Usar dados fictícios e serviços mock/sandbox. Definir fuso da operação com o dono, mantendo instante de importação com timezone e data bancária sem conversão indevida.
