# Migrations e banco

## Regras

1. Toda alteração de schema deve ter migration versionada junto ao código que a utiliza.
2. Escolher uma ferramenta/ORM na F05. Não habilitar sincronização automática de schema em nenhum ambiente.
3. Migration aplicada em ambiente compartilhado é imutável. Corrigir criando outra migration.
4. Separar migrations de schema, seeds fictícios e importação de dados reais.
5. Registrar versões aplicadas e falhar se conteúdo/histórico divergirem; implementar checksum quando a ferramenta não fornecer.
6. Aplicação não executa migrations no startup. Job único usa credencial DDL própria e bloqueio contra execução concorrente.
7. Evitar operações destrutivas automáticas. Colunas e tabelas antigas só são removidas em entrega posterior à transição.

## Validação obrigatória na CI

Em PostgreSQL descartável da mesma linha da produção:

- Criar banco vazio, aplicar todo o histórico e conferir schema/constraints.
- Reexecutar comando de aplicação: nenhuma migration pendente e nenhum efeito duplicado.
- Construir schema da última versão publicada e atualizá-lo para o candidato, preservando dados fictícios representativos.
- Detectar alteração em migration já publicada/aplicada; comparar com versão-base registrada.
- Exercitar constraints com inserts inválidos e imports concorrentes.

Antes da primeira release, a base de upgrade é uma versão aprovada do schema inicial. Testar reversão somente quando ela for suportada e não apagar dados; não exigir `down` destrutivo para toda mudança.

## Publicação

Usar expandir -> migrar dados -> trocar aplicação -> remover em entrega posterior. A aplicação anterior deve continuar operando com o schema expandido durante a promoção e eventual rollback.

Antes de mudanças grandes, estimar locks, duração, volume e espaço. Backfills grandes precisam ser retomáveis. Confirmar backup recuperável e plano específico. Migrations não devem imprimir dados sensíveis.

Se uma migration falhar: interromper a publicação, inspecionar seu estado e corrigir por procedimento registrado. Não executar `down`, reset, drop ou restaurar backup automaticamente.

## Banco de estudo existente

Exportar somente estrutura e conferir tabelas/constraints. Criar schema inicial em banco novo e descartável. Não apagar nem reutilizar automaticamente o banco de estudo. Se houver necessidade de importar dados locais, tratar como passo explícito separado e verificar contagens e totais. Identidades geradas devem ajustar suas sequências após importação.
