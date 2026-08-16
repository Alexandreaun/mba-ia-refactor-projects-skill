================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python 3 + Flask 3.1.1 (flask-cors 5.0.1), SQLite (sqlite3 stdlib)
Files:   4 analyzed | ~780 estimated lines of code

## Summary
CRITICAL: 4 | HIGH: 2 | MEDIUM: 3 | LOW: 4

## Findings

### [CRITICAL] Hardcoded Secrets & Configs
File: app.py:7-8, controllers.py:285-290
Description: `SECRET_KEY` está escrita em texto puro no código-fonte (`"minha-chave-super-secreta-123"`), `DEBUG` está fixado em `True`, e o endpoint `/health` (controllers.py:264-292) devolve `secret_key`, `debug` e `db_path` no corpo da resposta JSON para qualquer chamador não autenticado.
Impact: Qualquer pessoa com acesso à API (ou ao repositório) obtém a chave de assinatura de sessão/cookies e o caminho do banco; combinado com `DEBUG=True` em produção, um erro não tratado expõe o debugger interativo do Werkzeug, permitindo execução remota de código.
Recommendation: Mover `SECRET_KEY` e flags de ambiente para variáveis de ambiente (`os.environ["SECRET_KEY"]`), carregadas via `.env`/secret manager; nunca versionar segredos. Remover `secret_key`/`debug` do payload de `/health`.

### [CRITICAL] SQL Injection via concatenação de strings (sistêmico)
File: models.py:28, 47-50, 57-61, 68, 92, 109-111, 126-129, 140, 148-151, 155, 158-166, 174, 188, 192, 220, 224, 279-280, 289-297
Description: Praticamente toda função de acesso a dados em `models.py` monta comandos SQL concatenando strings com valores vindos diretamente da requisição (ex.: `"SELECT * FROM produtos WHERE id = " + str(id)`, `"...WHERE email = '" + email + "' AND senha = '" + senha + "'"`), sem parametrização (`?`) nem uso das APIs seguras do `sqlite3`.
Impact: Qualquer campo de entrada (id, nome, email, senha, termo de busca, categoria) pode ser usado para injetar SQL arbitrário, permitindo bypass de autenticação (`login_usuario`), leitura/alteração/exclusão de dados fora do escopo pretendido e exfiltração total do banco.
Recommendation: Substituir toda concatenação por queries parametrizadas com placeholders `?` do `sqlite3` (ex.: `cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))`), isolando essas chamadas em um Model/Repository.

### [CRITICAL] Endpoint de execução arbitrária de SQL sem autenticação
File: app.py:59-78
Description: A rota `POST /admin/query` recebe uma string SQL diretamente do corpo da requisição (`dados.get("sql")`) e a executa sem qualquer validação, sanitização ou controle de acesso (`cursor.execute(query)`), retornando inclusive os resultados de `SELECT`s arbitrários.
Impact: É, na prática, um console SQL público — permite leitura completa do banco (incluindo senhas em texto puro), alteração de qualquer tabela e destruição de dados (`DROP`/`DELETE`), sem autenticação nem log de auditoria.
Recommendation: Remover o endpoint por completo (não há caso de uso legítimo para expor SQL cru via API pública); se for indispensável para administração, restringir a operações pré-definidas expostas via Controller/Service com autenticação forte, autorização de role `admin` e allowlist de comandos.

### [CRITICAL] God Class / Monolithic Data Layer
File: models.py:1-315
Description: Um único módulo concentra todo o acesso a dados de 4 entidades de domínio distintas (produtos, usuários, pedidos, itens_pedido), com SQL cru inline, regras de checagem de estoque e cálculo de total de pedido (models.py:133-169), e lógica de relatório financeiro com regras de desconto (models.py:235-273) — tudo misturado sem separação por domínio (Repository) nem por responsabilidade (Model vs. Service).
Impact: Impossibilita teste unitário isolado de qualquer regra sem subir um banco SQLite real; qualquer alteração em uma entidade arrisca efeitos colaterais nas demais; viola Single Responsibility Principle.
Recommendation: Quebrar `models.py` em Models/Repositories por domínio (`ProdutoModel`, `UsuarioModel`, `PedidoModel`) e extrair regras de negócio (cálculo de total, checagem de estoque, desconto) para uma camada de Service, conforme o padrão "Controller → Service → Repository" do playbook.

### [HIGH] Fat Controllers / Regra de negócio no Controller
File: controllers.py:24-62 (criar_produto), 188-220 (criar_pedido), 237-255 (atualizar_status_pedido)
Description: `controllers.py` contém regras de negócio puras dentro das funções de rota: lista de categorias válidas hardcoded (linha 52), disparo de "notificações" (prints simulando envio de e-mail/SMS/push, linhas 208-210) e lógica condicional de notificação por status (linhas 247-250) — tudo no que deveria ser apenas a camada de orquestração HTTP.
Impact: A regra de negócio não pode ser testada sem simular uma requisição HTTP completa; duplicação inevitável se a mesma regra for necessária em outro ponto de entrada (ex.: um worker assíncrono).
Recommendation: Mover validação de domínio e efeitos colaterais de notificação para uma camada de Service (`PedidoService.criar`, `ProdutoService.validar`), deixando o Controller apenas repassar request → Service → response.

### [HIGH] Tight Coupling com conexão de banco global
File: database.py:4, 7-10; models.py:1 (import get_db em toda função); app.py:4, 49, 66
Description: `db_connection` é uma variável global mutável em nível de módulo, acessada via `get_db()` importado diretamente em `app.py`, `controllers.py` (indireto) e em toda função de `models.py`. Não há injeção de dependência: a conexão concreta com SQLite está fortemente acoplada a cada função consumidora.
Impact: Inviabiliza testes unitários com mocks/bancos em memória isolados por teste, cria risco de estado compartilhado entre requisições concorrentes, e impede trocar o backend de persistência sem reescrever todas as funções.
Recommendation: Encapsular a conexão em uma classe/factory injetável (ex.: `Database` passada ao construtor do Repository), permitindo substituição por mocks em testes, conforme o padrão de injeção de dependência do playbook.

### [MEDIUM] N+1 Query Problem
File: models.py:171-201 (get_pedidos_usuario), 203-233 (get_todos_pedidos)
Description: Para cada pedido retornado, o código executa uma query adicional para buscar `itens_pedido` e, para cada item, mais uma query para buscar o nome do produto (`cursor3`, linhas 191-193 e 223-225) — resultando em `1 + N + N*M` consultas ao invés de usar `JOIN`.
Impact: Degradação de performance proporcional ao número de pedidos/itens; em `listar_todos_pedidos` (usado por um endpoint sem paginação) o problema escala com todo o histórico de pedidos da loja.
Recommendation: Substituir os loops por uma única query com `JOIN` entre `pedidos`, `itens_pedido` e `produtos`, agrupando os resultados em memória, ou usar `WHERE pedido_id IN (...)` para buscar todos os itens em lote.

### [MEDIUM] Tratamento de erro duplicado e não centralizado
File: controllers.py (todas as 16 funções, ex.: 5-12, 14-22, 24-62, 136-144, 167-186, 257-262)
Description: Cada função do controller repete o mesmo bloco `try/except Exception as e: return jsonify({"erro": str(e)}), 500`, sem um error handler global do Flask (`@app.errorhandler`). Além disso, a mensagem crua da exceção (`str(e)`) é devolvida diretamente ao cliente.
Impact: Duplicação de código (16+ repetições do mesmo padrão) dificulta manutenção e padronização de respostas de erro; vazar `str(e)` ao cliente pode expor detalhes internos (nomes de tabelas, paths, stack info) — information disclosure.
Recommendation: Registrar um `@app.errorhandler(Exception)` central no Flask que loga o erro completo no servidor e retorna uma mensagem genérica e padronizada ao cliente; remover os `try/except` repetidos das funções individuais.

### [MEDIUM] Senhas armazenadas e comparadas em texto puro (API de segurança obsoleta/inexistente)
File: database.py:75-79 (seed), models.py:105-120 (login_usuario), models.py:122-131 (criar_usuario)
Description: Nenhuma função de hashing é aplicada às senhas — elas são inseridas em texto puro no banco (`"admin123"`, `"123456"`) e comparadas via `WHERE senha = '<texto puro>'` diretamente no SQL.
Impact: Equivalente a usar zero proteção criptográfica: qualquer vazamento do banco (incluindo via o próprio SQL injection acima) expõe as senhas reais de todos os usuários, que muitas vezes são reaproveitadas em outros sistemas.
Recommendation: Aplicar hashing forte com salt (bcrypt/Argon2) no momento do cadastro (`criar_usuario`) e comparar via `check_password_hash` no login, nunca comparando a senha em claro nem dentro da query SQL.

### [LOW] Magic Strings — listas de valores válidos hardcoded
File: controllers.py:52, 242
Description: A lista de categorias válidas (`["informatica", "moveis", ...]`, linha 52) e a lista de status de pedido válidos (`["pendente", "aprovado", "enviado", "entregue", "cancelado"]`, linha 242) são literais soltos dentro das funções, sem constante nomeada nem fonte única de verdade (o valor default `'pendente'` também está hardcoded separadamente em database.py:40).
Impact: Divergência silenciosa entre os valores aceitos em diferentes pontos do código é fácil de introduzir (ex.: esquecer de atualizar uma das duas listas), e não há reuso caso outra rota precise validar o mesmo conjunto.
Recommendation: Extrair para constantes/enum compartilhados (`CATEGORIAS_VALIDAS`, `STATUS_PEDIDO_VALIDOS`) em um módulo de constantes, importado onde for necessário.

### [LOW] Magic Numbers — limites e regras de desconto sem constantes semânticas
File: controllers.py:47-50; models.py:256-262
Description: Limites de tamanho de nome (`2`, `200`) em `controllers.py:47-50` e os limiares/percentuais de desconto do relatório de vendas (`10000`, `5000`, `1000`, `0.1`, `0.05`, `0.02`) em `models.py:256-262` são literais soltos sem nome semântico.
Impact: Regras de negócio importantes (política de desconto) ficam implícitas no meio de código de formatação de relatório, dificultando localizá-las, testá-las isoladamente ou alterá-las com segurança.
Recommendation: Extrair para constantes nomeadas (`NOME_MIN_LENGTH = 2`, `NOME_MAX_LENGTH = 200`, `DESCONTO_FAIXA_1_LIMIAR = 10000`, `DESCONTO_FAIXA_1_TAXA = 0.1`, etc.) declaradas no topo do módulo ou em um arquivo de configuração de regras de negócio.

### [LOW] Import não utilizado
File: database.py:2
Description: `import os` é declarado no topo do módulo, mas `os` nunca é referenciado em nenhum ponto de `database.py` (o caminho do banco é uma string literal fixa, `db_path = "loja.db"`, linha 5).
Impact: Poluição de código e ruído para quem lê o arquivo tentando entender as dependências reais do módulo; sinaliza falta de limpeza/lint no projeto.
Recommendation: Remover a linha `import os`, ou, se a intenção original era ler o caminho do banco de uma variável de ambiente, usar `os.environ.get("DB_PATH", "loja.db")` de fato.

### [LOW] Nomenclatura de parâmetro sombreando builtin da linguagem
File: controllers.py:14, 64, 98, 136
Description: As funções `buscar_produto(id)`, `atualizar_produto(id)`, `deletar_produto(id)` e `buscar_usuario(id)` usam `id` como nome de parâmetro, sombreando a função builtin `id()` do Python dentro do escopo dessas funções.
Impact: Reduz a legibilidade e pode causar bugs sutis caso `id()` built-in seja necessário dentro dessas funções no futuro (o nome deixa de estar disponível); é uma prática desencorajada pelos guias de estilo Python (PEP 8 / pylint `redefined-builtin`).
Recommendation: Renomear o parâmetro para algo semântico e não conflitante, ex.: `produto_id` / `usuario_id`, conforme já é feito em outras funções do mesmo arquivo (`listar_pedidos_usuario(usuario_id)`, `atualizar_status_pedido(pedido_id)`).

================================
Total: 13 findings
================================
