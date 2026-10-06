# Backlog ordenado

[Quadro e regras Kanban](kanban.md).

IDs F/B/W/X são referências internas. As 23 issues já estão publicadas, na mesma ordem: F01 #1, F02 #2, ..., X02 #23. Após integrar e validar F01, ela está concluída, F02 está em A fazer e as demais permanecem no Backlog. As evidências estão em [Configuração do GitHub](github-setup.md).

A fundação F01–F10 vem antes do código financeiro. O código financeiro evolui com banco e backend na mesma issue. O frontend começa depois de B05. B07 pode ocorrer em paralelo lógico com o restante do backend após B04, sem múltiplos agentes editando a mesma branch. X01/X02 são descoberta futura fora do MVP.

F09/F10 dependem de decisões de infraestrutura e RPO/RTO; não criar recursos pagos ou ligar operação real por suposição. A aprovação operacional final só acontece em W04.

| ID | Status | Prioridade | Fase | Tarefa | Dependências |
| --- | --- | --- | --- | --- | --- |
| F01 | Concluído | P0 | Fundação | Configurar repositório e regras do GitHub | Nenhuma |
| F02 | A fazer | P0 | Fundação | Iniciar backend e fixar ferramentas e versões | F01 |
| F03 | Backlog | P0 | Fundação | Validar configuração e separar ambientes | F02 |
| F04 | Backlog | P0 | Fundação | Subir PostgreSQL local e banco descartável de testes | F02, F03 |
| F05 | Backlog | P0 | Fundação | Criar mecanismo de migrations e instalação reproduzível | F04 |
| F06 | Backlog | P0 | Fundação | Completar CI com banco, testes e segurança | F02, F03, F04, F05 |
| F07 | Backlog | P0 | Fundação | Implementar autenticação e permissões | F06 |
| F08 | Backlog | P0 | Fundação | Adicionar auditoria e observabilidade | F07 |
| F09 | Backlog | P0 | Fundação | Preparar entrega em dev e staging | F06, F08 |
| F10 | Backlog | P0 | Fundação | Validar backup, recuperação e liberação de produção | F09 |
| B01 | Backlog | P1 | Backend e banco | Cadastrar e consultar contas bancárias | F07, F08, F10 |
| B02 | Backlog | P1 | Backend e banco | Registrar movimentações e regras de dinheiro | B01, F05 |
| B03 | Backlog | P1 | Backend e banco | Importar extratos por lote sem duplicar | B02 |
| B04 | Backlog | P1 | Backend e banco | Conciliar movimentações e mostrar divergências | B03 |
| B05 | Backlog | P1 | Backend e banco | Gerar resumo mensal e comparar meses | B04 |
| B06 | Backlog | P1 | Backend e banco | Conferir dados do legado para importação | B05 |
| B07 | Backlog | P2 | Backend e banco | Avaliar integração Bradesco com mock ou sandbox | B03, B04 |
| W01 | Backlog | P1 | Frontend | Iniciar Angular e conectar autenticação | B05, F07 |
| W02 | Backlog | P1 | Frontend | Criar telas de contas, importação e conciliação | W01, B01, B03, B04 |
| W03 | Backlog | P1 | Frontend | Exibir gráficos e relatórios mensais | W02, B05 |
| W04 | Backlog | P1 | Frontend | Homologar fluxo completo e liberar MVP | W03, B06, F10 |
| X01 | Backlog | P3 | Descoberta futura | Detalhar bot da prefeitura e viabilidade | Nenhuma |
| X02 | Backlog | P3 | Descoberta futura | Detalhar pagamentos automáticos e controles | B07, F10 |

## Critérios completos

### [F01] Configurar repositório e regras do GitHub

## Objetivo

Publicar a fundação e aplicar as regras reais do repositório.

## Dependências

Nenhuma.

## Critérios de aceite

- [ ] Repositório público conforme decisão do dono, com main, README, templates e documentação; Project privado.
- [ ] Workflow foundation executado com sucesso e check configurado conforme plano disponível.
- [ ] Squash, PR, bloqueio de force push/exclusão e resolução de conversas configurados onde suportados.
- [ ] Backlog aberto como issues com dependências; limitações de proteção registradas.

## Validação

Conferir visibilidade, SHA, execução de Actions e evidências das configurações em docs/github-setup.md.

### [F02] Iniciar backend e fixar ferramentas e versões

## Objetivo

Criar apps/api com NestJS e TypeScript estrito, sem módulos financeiros.

## Dependências

F01

## Critérios de aceite

- [ ] Node/npm/Nest/TypeScript/Jest e PostgreSQL verificados e versões exatas registradas; ORM decidido na F05.
- [ ] package-lock.json e configuração do runtime versionados; instalação com npm ci.
- [ ] ESLint, formatação, typecheck, build e testes configurados com comandos reais.
- [ ] Endpoint de saúde mínimo e teste com resposta esperada; sem passWithNoTests.

## Validação

Instalar do zero, executar lint/typecheck/build e testar saúde. Registrar versões e comandos no README.

### [F03] Validar configuração e separar ambientes

## Objetivo

Falhar cedo quando a configuração do ambiente estiver ausente, inválida ou incompatível.

## Dependências

F02

## Critérios de aceite

- [ ] Contrato .env.example atualizado com a estratégia real; secrets fora do Git.
- [ ] APP_ENV, portas, URLs, banco, CORS, TLS e secrets validados no startup.
- [ ] Testes rejeitam destino de produção e integrações reais; confirmar identidade do destino.
- [ ] Erros e logs não mostram credenciais; pagamentos desabilitados no MVP.

## Validação

Testar configurações válidas e inválidas de cada ambiente, placeholders e tentativa de conectar test a prod.

### [F04] Subir PostgreSQL local e banco descartável de testes

## Objetivo

Permitir desenvolver e testar banco/API com recursos isolados e reproduzíveis.

## Dependências

F02, F03

## Critérios de aceite

- [ ] Compose local com imagem fixada, porta em loopback, healthcheck e volume próprio.
- [ ] Banco test descartável por execução e sem acesso ao banco local/dev.
- [ ] Usuários de aplicação e migrations separados; secrets de exemplo são fictícios.
- [ ] Documentar comandos para criar/testar/remover somente recursos descartáveis; preservar banco de estudo.

## Validação

Inicializar local e test, conferir isolamento e permissões; demonstrar remoção do banco de teste sem afetar local.

### [F05] Criar mecanismo de migrations e instalação reproduzível

## Objetivo

Escolher uma única ferramenta/ORM e versionar o schema sem sincronização automática.

## Dependências

F04

## Critérios de aceite

- [ ] Decisão curta sobre ORM e migrations; synchronize/destructive reset desabilitados.
- [ ] Comandos reais para criar, aplicar e consultar estado das migrations.
- [ ] Histórico/checksum e exclusão mútua definidos; aplicação não faz DDL no startup.
- [ ] Instalação vazia e reexecução sem efeito duplicado; estratégia de upgrade validada.
- [ ] Banco de estudo preservado e plano de adaptação explícito; seeds fictícios separados.

## Validação

Aplicar migrations em PostgreSQL novo, reexecutar e testar alteração indevida no histórico. Validar upgrade de uma base aprovada.

### [F06] Completar CI com banco, testes e segurança

## Objetivo

Bloquear merge quando código, migrations ou validações essenciais falharem.

## Dependências

F02, F03, F04, F05

## Critérios de aceite

- [ ] Checks de lint, typecheck, unit, integration, migrations, build e security executam comandos reais.
- [ ] Integração usa PostgreSQL descartável; migrations testam banco vazio e upgrade.
- [ ] Scanner de segredos, dependências e workflows configurado; vulnerabilidades altas/críticas relevantes bloqueiam.
- [ ] required-checks falha em job ausente, cancelado ou com erro; sem mascarar falhas.
- [ ] Actions por SHA, menor privilégio e checks obrigatórios configurados no GitHub.

## Validação

PR válido passa; introduzir falha controlada em build, constraint, migration e scan para comprovar bloqueio. Remover as falhas antes do merge.

### [F07] Implementar autenticação e permissões

## Objetivo

Proteger a API antes de disponibilizar dados financeiros.

## Dependências

F06

## Critérios de aceite

- [ ] Estratégia de sessão/token documentada com hashing seguro de senha e validade/revogação.
- [ ] Perfis mínimos definidos com o dono e permissão por operação.
- [ ] Usuário inicial criado por procedimento seguro, sem senha fixa versionada.
- [ ] Tentativas de acesso inválidas limitadas e logs sem credenciais.

## Validação

Testar login válido/inválido, expiração/revogação e acesso negado por perfil; autenticação sozinha não basta.

### [F08] Adicionar auditoria e observabilidade

## Objetivo

Rastrear ações sensíveis e diagnosticar falhas sem expor dados pessoais.

## Dependências

F07

## Critérios de aceite

- [ ] Auditoria com ator, instante, ação e referência; identidade da aplicação não apaga histórico.
- [ ] Logs estruturados com correlação e redação de secrets/dados pessoais.
- [ ] Endpoints de health/liveness/readiness adequados sem divulgar detalhes privados.
- [ ] Alertas mínimos e regras de retenção/acesso documentados.

## Validação

Executar ação permitida e negada, conferir eventos, falha de banco e ausência de tokens/extratos nos logs.

### [F09] Preparar entrega em dev e staging

## Objetivo

Escolher infraestrutura e promover o mesmo artefato entre ambientes isolados.

## Dependências

F06, F08

## Critérios de aceite

- [ ] Hospedagem/registry/secrets escolhidos com orçamento e configuração documentada.
- [ ] Dev e staging com bancos, contas e redes próprios; apenas dados sintéticos ou anonimizados.
- [ ] Build gera SHA/digest/versão; promoção usa mesmo artefato com CI aprovada.
- [ ] Migrations executadas uma vez por ambiente com credencial separada; deploy serializado.
- [ ] Smoke tests e falha de promoção registrados; sem cancelar migrations em andamento.

## Validação

Publicar candidato em dev e staging; conferir digest igual, isolamento e bloqueio de candidato com CI reprovada.

### [F10] Validar backup, recuperação e liberação de produção

## Objetivo

Preparar produção com evidência de recuperação e aprovação humana.

## Dependências

F09

## Critérios de aceite

- [ ] RPO/RTO/retenção/responsável definidos com o dono e custos avaliados.
- [ ] Backup criptografado fora do host, monitorado e sem permissão de exclusão para a aplicação.
- [ ] Restauração em ambiente isolado mede tempo e valida schema, contagens e totais.
- [ ] Prod isolada; liberação explícita e mesmo digest aprovado em staging.
- [ ] Rollback de aplicação e procedimento de falha de migration documentados; sem restauração automática.

## Validação

Simular perda/falha com dados fictícios e comprovar recuperação dentro dos objetivos. Validar mecanismo real de aprovação; não lançar operações reais nesta issue.

### [B01] Cadastrar e consultar contas bancárias

## Objetivo

Entregar o primeiro módulo financeiro com migration, API e permissão.

## Dependências

F07, F08, F10

## Critérios de aceite

- [ ] Migration de contas com PK, campos obrigatórios e estado ativo/inativo.
- [ ] DTO, serviço e consultas parametrizadas; paginação e autorização.
- [ ] Dados fictícios Bradesco PJ para desenvolvimento; seeds fora de produção.
- [ ] Não excluir conta com histórico financeiro; auditar mudanças.

## Validação

Testar cadastro/consulta, payload inválido, perfil sem acesso e constraint de conta vinculada.

### [B02] Registrar movimentações e regras de dinheiro

## Objetivo

Persistir movimentações exatas, rastreáveis e vinculadas à conta.

## Dependências

B01, F05

## Critérios de aceite

- [ ] Migration com FK, valor NUMERIC positivo, tipo permitido e datas apropriadas.
- [ ] Identificador externo composto com conta quando presente; regra para origem sem ID.
- [ ] Decimal/string no contrato; rejeitar precisão indevida e campos inválidos.
- [ ] Preservar origem/histórico; correção autorizada e auditada.
- [ ] Regras aplicadas em serviço e banco, inclusive concorrência.

## Validação

Testar valores zero/negativos/limites, FK inválida, dinheiro exato, duplicidade concorrente e transações legítimas semelhantes.

### [B03] Importar extratos por lote sem duplicar

## Objetivo

Importar um formato de extrato confirmado a partir de amostra fictícia/sanitizada.

## Dependências

B02

## Critérios de aceite

- [ ] Formato escolhido após examinar amostra; limites de tamanho/linhas e parser seguro.
- [ ] Lote registra origem, referência, status, contagens e erros sem expor dados em logs.
- [ ] Reimportação/concorrência não duplicam movimentações; falha/retomada rastreáveis.
- [ ] Linhas ambíguas ficam visíveis para análise; não descartar somente por data/valor iguais.
- [ ] Arquivo real fica fora do Git e possui política de acesso/retenção.

## Validação

Importar arquivo válido, inválido, repetido e concorrente; simular falha parcial e retomada, comparando contagem e saldo.

### [B04] Conciliar movimentações e mostrar divergências

## Objetivo

Conferir registros com a fonte e manter pendências até a confirmação.

## Dependências

B03

## Critérios de aceite

- [ ] Estados e critérios de conciliação definidos com o dono.
- [ ] API lista pendências, confirma e registra divergências com justificativa/ator.
- [ ] Conferência respeita saldo inicial, entradas e saídas; transações atômicas.
- [ ] Histórico não é sobrescrito silenciosamente; permissão para correções.

## Validação

Validar exemplo 1000 + 200 + 300 - 150 = 1350; exercitar confirmação, divergência, correção e acesso negado.

### [B05] Gerar resumo mensal e comparar meses

## Objetivo

Expor totais consistentes para relatórios e gráficos futuros.

## Dependências

B04

## Critérios de aceite

- [ ] API com entradas, saídas, saldo e comparação de mês selecionado/anterior.
- [ ] Fuso, data de competência bancária e critérios das categorias definidos.
- [ ] Categorias financeiras com migrations/validações, se necessárias ao relatório.
- [ ] Total confere com movimentações e tratamento de pendências é explícito.
- [ ] Sem chamar saldo/fluxo de caixa de lucro contábil; consultas paginadas/indexadas conforme necessidade.

## Validação

Testar mês vazio, virada de ano/mês, categorias, pendências e soma exata com conjunto conhecido.

### [B06] Conferir dados do legado para importação

## Objetivo

Mapear e validar cópia dos dados antigos antes de migrá-los para operação.

## Dependências

B05

## Critérios de aceite

- [ ] Leitura da fonte sem alterar legado; mapear tabelas e regras financeiras.
- [ ] Ensaio com cópia autorizada fora do Git, origem e resultado rastreáveis.
- [ ] Comparar contagens, totais e divergências; normalizar datas/decimais explicitamente.
- [ ] Importação retomável/idempotente com relatório; aprovação operacional antes de dados reais.

## Validação

Usar amostra controlada, comparar registros/totais e simular reexecução. Documentar divergências sem publicar dados sensíveis.

### [B07] Avaliar integração Bradesco com mock ou sandbox

## Objetivo

Confirmar acesso, custos e contrato antes de ligar API bancária real.

## Dependências

B03, B04

## Critérios de aceite

- [ ] Verificar produto/acesso da conta PJ, endpoints, custos e limites disponíveis.
- [ ] Adaptador mock/sandbox com paginação, timeout, retries e deduplicação.
- [ ] Secrets por ambiente; test/staging sem conta real.
- [ ] Definir frequência de atualização e fechamento/conferência diária com o dono.
- [ ] Nenhum pagamento enviado; conexão real depende de autorização e ambiente preparado.

## Validação

Simular timeout, paginação, repetição e indisponibilidade; comparar com importação de arquivo. Se API não estiver disponível, registrar decisão e manter extrato.

### [W01] Iniciar Angular e conectar autenticação

## Objetivo

Criar o frontend depois da API validada, mantendo secrets no backend.

## Dependências

B05, F07

## Critérios de aceite

- [ ] Versões exatas e lockfile; lint/typecheck/build/test na CI sem checks fictícios.
- [ ] Configuração pública por ambiente, sem senha/token de banco embutido.
- [ ] Login, sessão/expiração e rotas protegidas; backend mantém autorização.
- [ ] Interface simples, acessível e com erros/estados de carregamento.

## Validação

Testar sessão expirada, acesso negado e build reproduzível; inspecionar bundle para ausência de secrets.

### [W02] Criar telas de contas, importação e conciliação

## Objetivo

Permitir consultar dados e resolver pendências com feedback claro.

## Dependências

W01, B01, B03, B04

## Critérios de aceite

- [ ] Listagens com filtros/paginação e valores monetários corretos.
- [ ] Upload limitado com resultado por lote, erros e proteção contra envio duplicado.
- [ ] Pendências/divergências visíveis e confirmação autorizada com justificativa.
- [ ] Estados vazios, falhas de rede e navegação por teclado tratados.

## Validação

Fluxo E2E de importar, reimportar, conferir pendência e conciliar; usuário sem permissão recebe bloqueio na API.

### [W03] Exibir gráficos e relatórios mensais

## Objetivo

Apresentar comparações confiáveis com base na API financeira.

## Dependências

W02, B05

## Critérios de aceite

- [ ] Mês selecionado/anterior com entradas, saídas e saldo coerentes.
- [ ] Gráfico e tabela exibem mesma fonte de dados e filtros.
- [ ] Pendências, valores ausentes e período vazio identificados.
- [ ] Exportação inicial definida com o dono, sem inventar documentos fiscais/contábeis.

## Validação

Conferir totais da tela, tabela e API com dataset conhecido; testar virada de ano e ausência de movimento.

### [W04] Homologar fluxo completo e liberar MVP

## Objetivo

Validar a primeira entrega com o dono e evidência de operação/recuperação.

## Dependências

W03, B06, F10

## Critérios de aceite

- [ ] E2E autenticação -> importação -> conciliação -> relatório em staging.
- [ ] Dono valida totais/fluxo; pendências e limites documentados.
- [ ] Restauração, monitoramento e procedimento de suporte conferidos.
- [ ] Release/tag/changelog e promoção do mesmo digest após aprovação explícita.
- [ ] Integração bancária por API é opcional conforme B07; extrato é caminho válido do MVP.

## Validação

Registrar evidências sintéticas de homologação, recuperação e release. Smoke tests de prod sem movimentar dinheiro real.

### [X01] Detalhar bot da prefeitura e viabilidade

## Objetivo

Descobrir a automação de requisições solicitada pelo dono sem expandir o MVP silenciosamente.

## Dependências

Nenhuma.

## Critérios de aceite

- [ ] Identificar portal, ações necessárias, autorização de acesso, dados e custo.
- [ ] Verificar API oficial, MFA/CAPTCHA/limites e termos de operação.
- [ ] Definir alternativa manual, auditoria e gestão segura de credenciais.
- [ ] Aprovar escopo separado antes de implementação; nenhuma credencial no Git.

## Validação

Produzir descrição do fluxo e orçamento com evidência autorizada. Não ativar bot nesta issue.

### [X02] Detalhar pagamentos automáticos e controles

## Objetivo

Confirmar necessidade e controles antes de qualquer envio de pagamentos.

## Dependências

B07, F10

## Critérios de aceite

- [ ] Dono confirma se pagamentos são necessários e quais tipos.
- [ ] Definir aprovações, limites, segregação de funções e dupla confirmação.
- [ ] Propor idempotência, estados, conciliação pós-envio e tratamento de retorno incerto.
- [ ] Usar apenas sandbox na prova futura; autorização específica antes de dinheiro real.

## Validação

Documento com fluxo, riscos, custos e critérios de aceite para uma etapa futura; sem chamar endpoint real de pagamento.
