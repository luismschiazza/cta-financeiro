# Backup e recuperação

## Antes de usar dados reais

Definir com o dono: perda máxima tolerável de dados (RPO), tempo máximo de recuperação (RTO), retenção, responsável, orçamento e procedimento de incidente. Não prometer recuperação sem essas definições e um teste demonstrável.

Backup deve ser automatizado, criptografado, monitorado e armazenado fora do host principal. A identidade da aplicação não pode apagar os backups. Avaliar retenção imutável/versionada no provedor escolhido.

## Exercício obrigatório

1. Gerar backup com dados sintéticos.
2. Restaurar em banco/host independente sem sobrescrever produção.
3. Conferir schema, migrations, usuários autorizados, contagens, totais e conciliação.
4. Registrar duração, idade do ponto restaurado, resultado e responsável.
5. Verificar RPO/RTO definidos e corrigir diferenças.

A frequência de backup e restauração será decidida conforme esses objetivos. Snapshot da máquina sozinho pode não cobrir falha do provedor ou credenciais comprometidas. Se RPO exigir recuperação pontual, avaliar backups base e arquivamento de WAL ou serviço gerenciado equivalente.

## Incidente

Suspender operações afetadas, preservar evidências, determinar último ponto íntegro e obter decisão operacional. Restauração é uma intervenção controlada com possível perda de dados; nunca parte automática de rollback de aplicação. Após restaurar, reconciliar movimentações posteriores com a fonte bancária e registrar divergências.

Logs técnicos não incluem tokens, senhas, documentos ou extratos completos. Auditoria financeira registra ator, ação, instante e referência com acesso e retenção específicos.
