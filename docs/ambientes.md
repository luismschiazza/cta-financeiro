# Ambientes e configuração

## Isolamento obrigatório

| Ambiente | Banco sugerido | Identidade de aplicação | Provisionamento |
| --- | --- | --- | --- |
| local | cta_financeiro_local | cta_app_local | Docker Compose na máquina |
| dev | cta_financeiro_dev | cta_app_dev | Serviço independente |
| test | cta_financeiro_test_<run_id> | cta_app_test | Descartável por execução |
| staging | cta_financeiro_staging | cta_app_staging | Serviço independente |
| prod | cta_financeiro_prod | cta_app_prod | Serviço restrito |

Os nomes são convenções; também isolar hosts/instâncias, redes e secrets. Nome diferente no mesmo servidor não basta como barreira. O banco de estudo `cta_financeiro_dev` permanece isolado até a adaptação definida em F05.

Aplicação usa usuário de privilégio mínimo. Migrations usam identidade separada com DDL. Produção não aceita conexões dos testes ou do desenvolvimento.

## Variáveis

`.env.example` é um contrato proposto, sem credenciais. Copiar para `.env` local e preencher apenas valores fictícios. Não usar o exemplo em produção. Nenhum carregador de configuração foi implementado ainda.

Na F03, validar ao iniciar:

- `APP_ENV` em local/dev/test/staging/prod; `NODE_ENV` coerente com modo de execução.
- Porta inteira válida, URL do frontend, host e porta do banco, nome do banco e usuários obrigatórios.
- Credenciais ausentes ou placeholders provocam falha sem imprimir seus valores.
- TLS obrigatório para banco remoto fora de local/test; validar certificado.
- Origens CORS explícitas; não usar wildcard com credenciais.
- Sessão/autenticação só inicia com secrets adequados à estratégia escolhida.
- `BANK_INTEGRATION_MODE=mock` por padrão; ambiente test rejeita modo real.
- `PAYMENTS_ENABLED=false` no MVP; frontend nunca recebe secrets do backend.

Checar também ambiente declarado no banco/infraestrutura. Prefixo no nome do banco é uma proteção auxiliar, não uma prova de isolamento.

## Produção

Secrets do provedor ou do GitHub, conforme disponibilidade do plano. Preferir identidade temporária/OIDC onde suportado. Nunca compartilhar tokens bancários ou contas da prefeitura entre ambientes. Staging usa sandbox ou mocks.

A configuração de cinco ambientes é o padrão; só local e test serão necessários para começar a programar. Provisionar dev, staging e prod conforme F09/F10 e decisão de hospedagem. Não criar recursos pagos por suposição.
