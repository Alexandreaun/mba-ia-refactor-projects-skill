================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python 3 + Flask 3.1.1 (flask-cors 5.0.1, python-dotenv 1.0.1), SQLite (sqlite3 stdlib)
Files:   25 analyzed | ~883 estimated lines of code

## Summary
CRITICAL: 0 | HIGH: 0 | MEDIUM: 2 | LOW: 2

## Nota sobre a cota de severidade
Esta é a 3ª rodada de auditoria sobre este projeto (rodadas anteriores já resolveram: hardcoded secrets, SQL injection, endpoint de SQL arbitrário, God Class em models.py/controllers.py, N+1 em pedidos, controller acessando o banco diretamente, tight coupling com o serviço de notificação, e validações duplicadas/ausentes). Uma nova varredura completa contra os 11 itens do catálogo — incluindo verificação explícita de Hardcoded Secrets (`.env` real está corretamente fora do git via `.gitignore` na raiz do repositório; `SECRET_KEY` vem de variável de ambiente), God Class, Fat Controller, Tight Coupling e Sync/Async — não encontrou nenhuma ocorrência genuína de severidade CRITICAL ou HIGH remanescente no código atual. Reportar um achado nessas severidades sem uma correspondência real ao catálogo violaria a regra de "Sem Subjetividade" da própria auditoria. Os 4 achados abaixo (2 MEDIUM, 2 LOW) são reais, reproduzidos e precisos; nenhum item foi inflado para atingir a cota.

## Findings

### [MEDIUM] TypeError não tratado em validação de produto com tipos inválidos
File: models/produto_model.py:83-84
Description: `ProdutoModel.validar_dados` compara `preco < 0` e `estoque < 0` sem antes confirmar que são numéricos. Se o cliente enviar `"preco": "abc"` (string), a comparação `str < int` lança `TypeError` em vez de retornar uma mensagem de validação.
Impact: Reproduzido via `curl -X POST /produtos -d '{"nome":"X","preco":"abc","estoque":1}'`: retorna `500 {"erro":"Erro interno no servidor"}` (stack trace nos logs) em vez de `400` com mensagem de validação clara — o mesmo problema de "input não validado vira erro interno" já corrigido em outros pontos do controller nesta rodada anterior, mas que persiste na camada de Model.
Recommendation: Validar o tipo antes da comparação, ex.: `if not isinstance(preco, (int, float)) or preco < 0: return "Preço inválido"` (idem para `estoque`), retornando erro de validação em vez de deixar o `TypeError` propagar.

### [MEDIUM] TypeError não tratado ao criar pedido com quantidade inválida
File: models/pedido_model.py:32
Description: `PedidoModel.criar` compara `produto["estoque"] < item["quantidade"]` sem validar que `quantidade` é numérica.
Impact: Reproduzido via `curl -X POST /pedidos -d '{"usuario_id":1,"itens":[{"produto_id":1,"quantidade":"abc"}]}'`: retorna `500 {"erro":"Erro interno no servidor"}` em vez de `400`, mesma classe de problema do achado acima, desta vez no fluxo de criação de pedidos.
Recommendation: Validar `item["quantidade"]` (inteiro positivo) em `PedidoController.criar_pedido` antes de repassar ao Model, retornando `error("Quantidade inválida para o item", 400)` quando o tipo/valor for inválido.

### [LOW] Magic strings de status de pedido no serviço de notificação
File: services/notification_service.py:13, 15
Description: `notificar_mudanca_status` compara `novo_status == "aprovado"` e `novo_status == "cancelado"` com literais soltos, apesar de `constants.py` já definir `STATUS_APROVADO`/`STATUS_CANCELADO` (usados em `pedido_model.py` desde a rodada anterior de refatoração).
Impact: Fonte de verdade duplicada para os mesmos valores; um erro de digitação neste arquivo não seria pego por nenhuma validação e silenciosamente pararia de disparar a notificação correta.
Recommendation: Importar e usar `STATUS_APROVADO`/`STATUS_CANCELADO` de `constants.py` neste arquivo, como já feito em `models/pedido_model.py`.

### [LOW] Defaults de schema SQL duplicando constantes já existentes
File: models/database.py:46, 54
Description: O DDL de `_create_schema` usa `tipo TEXT DEFAULT 'cliente'` (linha 46) e `status TEXT DEFAULT 'pendente'` (linha 54) como literais SQL soltos, embora `TIPO_USUARIO_PADRAO` e `STATUS_PENDENTE` já existam em `constants.py` e sejam usados em Python nos mesmos módulos relacionados.
Impact: Divergência de fonte de verdade entre o valor usado pela aplicação (`UsuarioModel.criar`, `PedidoModel.criar`) e o `DEFAULT` do schema, que só se aplica se algum INSERT futuro omitir a coluna — risco baixo, mas inconsistente com o padrão já adotado no restante do projeto.
Recommendation: Interpolar as constantes na string do DDL (ex.: `f"tipo TEXT DEFAULT '{TIPO_USUARIO_PADRAO}'"`) para manter uma única fonte de verdade.

================================
Total: 4 findings
================================
