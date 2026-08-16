================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python 3 + Flask 3.1.1 (flask-cors 5.0.1, python-dotenv 1.0.1), SQLite (sqlite3 stdlib)
Files:   24 analyzed | ~835 estimated lines of code

## Summary
CRITICAL: 0 | HIGH: 1 | MEDIUM: 2 | LOW: 2

## Findings

### [HIGH] Fat Controller / Direct DB manipulation in Controller
File: controllers/admin_controller.py:26-63
Description: `AdminController.reset_database` (26-35) e `AdminController.health_check` (37-63) recebem a instância `Database` diretamente e executam SQL cru (`DELETE FROM ...`, `SELECT COUNT(*) FROM ...`) dentro do Controller, em vez de delegar essas operações a um Model/Repository, como os demais controllers (`ProdutoController`, `UsuarioModel` etc.) já fazem.
Impact: Quebra a separação de camadas MVC já estabelecida no restante do projeto — a lógica de acesso a dados fica acoplada ao Controller, dificultando testes unitários sem um banco real e criando inconsistência arquitetural (esta é a única classe de Controller que fala SQL diretamente).
Recommendation: Extrair as operações para um `AdminModel`/`AdminRepository` (ex.: `db.reset_all()`, `db.get_counts()`) injetado no Controller, seguindo o mesmo padrão de injeção de dependência já usado por `ProdutoModel`, `UsuarioModel` e `PedidoModel`.

### [MEDIUM] N+1 Query Problem em criação de pedido
File: models/pedido_model.py:21-29
Description: `PedidoModel.criar` executa um `SELECT * FROM produtos WHERE id = ?` dentro de um laço `for item in itens` (uma consulta por item do pedido) para validar estoque e montar o total, em vez de buscar todos os produtos envolvidos em uma única consulta.
Impact: Para pedidos com muitos itens, o número de round-trips ao banco cresce linearmente (N+1), aumentando a latência do endpoint `POST /pedidos` proporcionalmente à quantidade de itens.
Recommendation: Coletar todos os `produto_id` do pedido e buscar em lote com `SELECT * FROM produtos WHERE id IN (?, ?, ...)` (mesmo padrão de `placeholders` já usado em `_listar`, models/pedido_model.py:70-71), montando um dicionário `produtos_por_id` a partir do resultado único.

### [MEDIUM] Validação de negócio duplicada entre métodos do Controller
File: controllers/produto_controller.py:21-51, 53-81
Description: `criar_produto` (21-51) e `atualizar_produto` (53-81) reimplementam, de forma quase idêntica e descentralizada, a mesma cadeia de validações (`dados` ausente, campos obrigatórios, `preco`/`estoque` negativos) chamando `error(...)` a cada checagem, em vez de centralizar essa validação em um schema/validator compartilhado.
Impact: Qualquer alteração de regra (ex.: novo campo obrigatório, novo limite) precisa ser replicada manualmente em múltiplos pontos; o risco de divergência entre `criar_produto` e `atualizar_produto` já existe hoje (`atualizar_produto` não revalida `NOME_PRODUTO_MIN_LENGTH`/`MAX_LENGTH` nem `CATEGORIAS_VALIDAS`, ao contrário de `criar_produto`).
Recommendation: Extrair a validação para uma função/schema único (ex.: `validar_produto(dados, parcial=False)`) reaproveitado pelos dois métodos, retornando uma lista de erros consolidada — elimina a duplicação e garante paridade de regras entre criação e atualização.

### [LOW] Magic strings de status de pedido fora das constantes existentes
File: models/pedido_model.py:32, 116, 119, 122
Description: O projeto já define `STATUS_PEDIDO_VALIDOS = ["pendente", "aprovado", "enviado", "entregue", "cancelado"]` em `constants.py`, mas `PedidoModel` usa os literais `'pendente'`, `'aprovado'` e `'cancelado'` diretamente nas queries SQL (INSERT e `relatorio_vendas`) em vez de referenciar essas constantes.
Impact: Um erro de digitação em um desses literais SQL não seria pego por nenhuma validação e geraria contagens silenciosamente erradas no relatório de vendas.
Recommendation: Referenciar os valores de `STATUS_PEDIDO_VALIDOS` (por índice ou nome) ao montar as queries, garantindo uma única fonte de verdade para os status válidos.

### [LOW] Valor padrão "geral" duplicado sem constante nomeada
File: controllers/produto_controller.py:37, 73
Description: O literal `"geral"` (categoria padrão de um produto) aparece hardcoded duas vezes (`criar_produto` e `atualizar_produto`), apesar de `constants.py` já centralizar `CATEGORIAS_VALIDAS`.
Impact: Se a categoria padrão mudar, é preciso lembrar de atualizar os dois pontos manualmente; risco de divergência baixo, mas evitável.
Recommendation: Adicionar `CATEGORIA_PADRAO = "geral"` em `constants.py` e referenciá-la nos dois métodos.

================================
Total: 5 findings
================================
