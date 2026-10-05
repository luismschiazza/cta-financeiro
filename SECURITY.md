# Segurança

Projeto privado em desenvolvimento; ainda não há versão operacional com suporte definido.

Relatar suspeitas de vulnerabilidade de forma privada ao responsável pelo repositório. Não incluir dados de pacientes, extratos reais, secrets ou exploits com credenciais em issues e logs.

Antes de operar: autenticação, autorização por operação, validação estrita, TLS remoto, consultas parametrizadas, auditoria, limites de requisição/importação e backup testado. A aplicação não recebe privilégios de administrador do banco.

Se um secret vazar, revogar/rotacionar e investigar. Remover o arquivo do último commit não apaga o histórico nem resolve o comprometimento. Nunca depender apenas de `.gitignore` ou de um scanner.

Banco, prefeitura e outros serviços reais só serão conectados após validar autorização, acesso, contrato e forma de manter credenciais. Pagamentos automáticos não pertencem ao MVP.
