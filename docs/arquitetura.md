# Arquitetura

## Decisão inicial

Monólito modular: uma API NestJS, um banco PostgreSQL por ambiente e, posteriormente, uma aplicação Angular. Não introduzir microserviços antes de existir uma necessidade operacional demonstrada.

A estrutura prevista é `apps/api`, `apps/web`, `docs`, `scripts` e `.github`. Neste pacote, apenas documentação e ferramentas da fundação existem.

## Responsabilidades

- Controller: autenticação/autorização e entrada HTTP por DTO validado.
- Serviço: regras de negócio, transações e decisões de conciliação.
- Persistência: consultas parametrizadas e constraints do banco.
- Adaptador externo: importar banco/legado sem acoplar o domínio ao fornecedor.

Uma entrada válida no controller não permite dispensar validação do serviço e do banco. Jobs, imports e scripts também passam pelas mesmas regras financeiras.

## Módulos previstos

Configuração; identidade/acesso; auditoria; contas; movimentações; categorias; importações; conciliação; relatórios. Pagamentos e prefeitura têm descoberta separada e não entram no MVP.

## Dados e concorrência

Valores monetários em `NUMERIC` com escala definida. No TypeScript e JSON, transportar dinheiro como string decimal ou objeto decimal escolhido; não somar dinheiro com ponto flutuante binário. Transações do banco agrupam operações que precisam ocorrer juntas.

A unicidade de movimentação bancária será composta pela conta e pelo identificador externo, quando fornecido pela origem. Imports concorrentes devem usar essa proteção no banco, sem depender apenas de uma consulta prévia.

Quando um formato não fornecer identificador confiável, documentar a estratégia de identidade e separar possíveis duplicatas para análise. Data, nome e valor iguais não provam que duas movimentações são a mesma.

## Histórico e operação

Registro bancário importado conserva origem e referência. Correções de conciliação devem deixar histórico; não sobrescrever silenciosamente o passado. Auditoria financeira é diferente de log técnico e possui retenção e permissões próprias.

Backups independentes e testes de restauração fazem parte da operação. Um arquivo do dia anterior não substitui backup nem garante imutabilidade.
