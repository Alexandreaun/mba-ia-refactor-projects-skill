================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python 3 + Flask 3.1.1 (flask-cors 5.0.1, python-dotenv 1.0.1), SQLite (sqlite3 stdlib)
Files:   25 analyzed | ~858 estimated lines of code

## Summary
CRITICAL: 0 | HIGH: 1 | MEDIUM: 2 | LOW: 2

## Findings

### [HIGH] Tight Coupling entre Controller e serviço de notificação
File: controllers/pedido_controller.py:4, 30, 50
Description: `PedidoController` importa as funções concretas `notificar_pedido_criado`/`notificar_mudanca_status` diretamente do módulo `services.notification_service` (linha 4) e as invoca inline em `criar_pedido` (linha 30) e `atualizar_status_pedido` (linha 50), em vez de receber um serviço/notificador injetado no construtor.
Impact: O Controller fica acoplado à implementação concreta do serviço de notificação; testar `PedidoController` isoladamente (sem monkeypatch do módulo) ou trocar o canal de notificação (e-mail/SMS real, fila, etc.) exige alterar o Controller em vez de apenas injetar outra implementação.
Recommendation: Definir uma interface/protocolo de notificação e injetá-la via construtor (`PedidoController(self, pedido_model, notificador)`), seguindo o mesmo padrão de injeção de dependência já usado para `pedido_model` em todos os Controllers.

### [MEDIUM] Corpo JSON ausente/nulo derruba endpoints com 500 em vez de 400
File: controllers/usuario_controller.py:36-39, controllers/pedido_controller.py:42-44
Description: `UsuarioController.login` e `PedidoController.atualizar_status_pedido` chamam `dados.get(...)` imediatamente após `request.get_json()` sem checar `if not dados`, ao contrário de `criar_usuario` e `criar_pedido`, que já fazem essa validação. Quando o corpo é `null`/ausente (JSON válido representando `None`), `dados` é `None` e `dados.get(...)` lança `AttributeError`.
Impact: Reproduzido via `curl -X POST /login -d 'null' -H "Content-Type: application/json"` e `curl -X PUT /pedidos/1/status -d 'null' -H "Content-Type: application/json"`: ambos retornam `500 {"erro":"Erro interno no servidor"}` em vez do `400` de validação esperado, escondendo a causa real do erro do cliente da API e poluindo os logs com stack traces para uma entrada simplesmente inválida.
Recommendation: Adicionar a mesma guarda `if not dados: return error("Dados inválidos", 400)` no início de `login` e `atualizar_status_pedido`, alinhando com o padrão já usado em `criar_usuario`/`criar_pedido` (idealmente centralizando em um helper compartilhado, ver achado anterior sobre validação duplicada).

### [MEDIUM] Conversão de query params sem tratamento de erro
File: controllers/produto_controller.py:72-75
Description: `buscar_produtos` converte `preco_min`/`preco_max` com `float(preco_min)`/`float(preco_max)` sem `try/except` nem validação de formato numérico.
Impact: Reproduzido via `curl "/produtos/busca?preco_min=abc"`: retorna `500 {"erro":"Erro interno no servidor"}` (stack trace de `ValueError` nos logs) em vez de um `400` informando que o parâmetro é inválido — um erro de digitação do cliente derruba a requisição como falha interna do servidor.
Recommendation: Envolver a conversão em `try/except ValueError` retornando `error("preco_min/preco_max deve ser numérico", 400)`, ou validar o formato antes de converter.

### [LOW] Campo "ambiente" do health check hardcoded
File: controllers/admin_controller.py:40
Description: `health_check` sempre retorna `"ambiente": "producao"`, independentemente da configuração real (`Config.DEBUG`/variável de ambiente), tanto em desenvolvimento quanto produção.
Impact: A resposta de `/health` informa incorretamente o ambiente quando a aplicação roda em modo debug/local, podendo confundir monitoramento e automações que decidem comportamento com base nesse campo.
Recommendation: Derivar o valor a partir de `Config` (ex.: `"ambiente": "desenvolvimento" if Config.DEBUG else "producao"`) ou de uma variável de ambiente dedicada (`APP_ENV`).

### [LOW] Papel de usuário padrão como string solta
File: models/usuario_model.py:19
Description: `UsuarioModel.criar` usa o literal `"cliente"` como valor padrão do parâmetro `tipo`, sem uma constante nomeada — mesmo padrão que `constants.py` já resolveu para categorias de produto (`CATEGORIA_PADRAO`) e status de pedido (`STATUS_*`).
Impact: Divergência de padrão dentro do próprio projeto; qualquer verificação futura de papel (ex.: `if usuario["tipo"] == "cliente"`) precisaria repetir a string em vários lugares sem uma fonte única de verdade.
Recommendation: Adicionar `TIPO_USUARIO_PADRAO = "cliente"` (e opcionalmente `TIPO_USUARIO_ADMIN = "admin"`) em `constants.py` e referenciar em `usuario_model.py`.

================================
Total: 5 findings
================================
