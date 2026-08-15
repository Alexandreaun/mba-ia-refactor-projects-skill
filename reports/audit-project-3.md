================================
ARCHITECTURE AUDIT REPORT
================================
Project: task-manager-api
Stack:   Python 3.11 + Flask 3.0 (Blueprints) + Flask-SQLAlchemy
Files:   15 analyzed | ~1170 estimated lines of code

## Summary
CRITICAL: 2 | HIGH: 2 | MEDIUM: 3 | LOW: 3

## Findings

### [CRITICAL] Hardcoded Secrets & Configs
File: app.py:13; services/notification_service.py:9-10
Description: `app.config['SECRET_KEY'] = 'super-secret-key-123'` está escrito diretamente no código-fonte; `NotificationService.__init__` grava `email_user = 'taskmanager@gmail.com'` e `email_password = 'senha123'` também em texto plano, apesar do projeto já declarar `python-dotenv` em `requirements.txt` (nunca utilizado).
Impact: Vazamento do repositório expõe a chave de assinatura de sessão do Flask (permitindo forjar cookies/CSRF) e credenciais de uma conta de e-mail real.
Recommendation: Carregar `SECRET_KEY`, `EMAIL_USER` e `EMAIL_PASSWORD` via `os.environ` (usando `python-dotenv` para popular `.env` local), nunca commitados.

### [CRITICAL] God Class / Monolithic Route Files
File: routes/task_routes.py:1-300 (mesmo padrão em routes/user_routes.py:1-212 e routes/report_routes.py:1-224)
Description: Cada blueprint mistura roteamento HTTP, validação de regras de negócio (tamanho de título, status/priority válidos), cálculo de domínio (overdue) e acesso direto ao ORM (`Task.query`, `User.query`, `Category.query`) na mesma função, sem nenhuma camada de serviço interposta — `services/` existe mas não é usado por nenhuma rota.
Impact: Impossível testar uma regra de negócio isoladamente do Flask/DB; qualquer alteração de regra exige tocar o mesmo arquivo que define a rota HTTP, violando Single Responsibility em todo o módulo de rotas.
Recommendation: Extrair regras de negócio para `/services` (`TaskService`, `UserService`, `ReportService`) e regras puras para `/models`; as rotas devem apenas orquestrar request → service → response.

### [HIGH] Fat Controllers / Lógica de Negócio Duplicada nas Rotas
File: routes/task_routes.py:30-39,71-80; routes/user_routes.py:171-180; routes/report_routes.py:33-37,132-135
Description: O cálculo de "overdue" (`due_date < utcnow()` e `status` fora de `done`/`cancelled`) é reimplementado manualmente com o mesmo bloco `if/else` em 5 pontos diferentes das rotas, embora o Model `Task` já exponha o método equivalente `is_overdue()` (models/task.py:50-60).
Impact: Qualquer correção na regra de atraso precisa ser replicada manualmente em 5 lugares; alto risco de divergência entre endpoints (um endpoint corrigido e outro esquecido).
Recommendation: Remover a lógica duplicada nas rotas e chamar `task.is_overdue()`; a regra de negócio deve morar apenas no Model/Service, e a rota apenas consome o resultado.

### [HIGH] Tight Coupling em NotificationService
File: services/notification_service.py:5-10
Description: `NotificationService.__init__` instancia a configuração de SMTP (host, porta, usuário, senha) diretamente como atributos fixos da classe, e o próprio `smtplib.SMTP` é instanciado diretamente dentro de `send_email` — sem nenhuma rota do projeto injetar ou chamar essa classe.
Impact: Impossibilita testar/mocking do envio de e-mail e trocar de provedor sem editar a classe; a dependência de infraestrutura (SMTP) fica soldada à lógica de notificação.
Recommendation: Receber configuração (host/porta/credenciais) via injeção no construtor, lida de variáveis de ambiente, e injetar um client de e-mail (ou interface) em vez de instanciar `smtplib.SMTP` diretamente dentro do método.

### [MEDIUM] N+1 Query Problem
File: routes/task_routes.py:41-57; routes/report_routes.py:55-68
Description: `get_tasks()` executa `User.query.get(t.user_id)` e `Category.query.get(t.category_id)` dentro do loop `for t in tasks`; `summary_report()` executa `Task.query.filter_by(user_id=u.id).all()` dentro do loop `for u in users`.
Impact: O número de consultas ao banco cresce linearmente com a quantidade de tasks/usuários, degradando performance conforme a base de dados cresce.
Recommendation: Usar eager loading do SQLAlchemy (`Task.query.options(joinedload(Task.user), joinedload(Task.category)).all()`) ou uma única consulta com `JOIN`, agregando os resultados em memória em vez de repetir queries por item do loop.

### [MEDIUM] Swallowed Exceptions / Duplicated Error Handling
File: routes/task_routes.py:62-63; routes/user_routes.py:130-132,149-151; routes/report_routes.py:186-188,207-209,221-223
Description: `get_tasks()` usa um `except:` genérico que descarta o erro original e retorna apenas `{'error': 'Erro interno'}`; praticamente toda rota de escrita repete seu próprio bloco `try/except/db.session.rollback()` com mensagem própria, sem nenhum handler central.
Impact: A causa raiz de falhas de banco fica invisível (nem sequer logada), e a duplicação do padrão try/rollback em cerca de 9 funções aumenta o risco de inconsistência entre respostas de erro.
Recommendation: Capturar o erro real (`except Exception as e`) e logá-lo, propagando-o para um `@app.errorhandler` global do Flask que padroniza a resposta e centraliza o rollback.

### [MEDIUM] Deprecated/Unsafe API — Hash de Senha com MD5
File: models/user.py:27-32
Description: `set_password`/`check_password` usam `hashlib.md5` sem salt para armazenar e comparar a senha do usuário.
Impact: MD5 é criptograficamente quebrado; em caso de vazamento do banco, senhas são recuperáveis trivialmente via rainbow tables/força bruta.
Recommendation: Substituir por `werkzeug.security.generate_password_hash` / `check_password_hash` (já disponível como dependência transitiva do Flask) ou por `bcrypt`/`argon2`.

### [LOW] Magic Strings — Listas de Status/Role Duplicadas
File: routes/task_routes.py:110,177; routes/user_routes.py:71,120; models/task.py:39; utils/helpers.py:75,110-111
Description: A lista literal `['pending', 'in_progress', 'done', 'cancelled']` e `['user', 'admin', 'manager']` é reescrita em pelo menos 5 lugares diferentes, apesar de `utils/helpers.py:110-111` já declarar `VALID_STATUSES`/`VALID_ROLES` — constantes que nunca são importadas nem usadas em nenhum arquivo.
Impact: Adicionar um novo status ou role exige localizar e editar manualmente todas as ocorrências; a constante já existente fica órfã e desatualizada por não ser reaproveitada.
Recommendation: Importar e usar `VALID_STATUSES`/`VALID_ROLES` de `utils/helpers.py` em todos os pontos de validação, eliminando as listas literais duplicadas.

### [LOW] Nomenclatura de Variáveis Inconsistente
File: routes/task_routes.py:16; routes/user_routes.py:14; routes/report_routes.py:161
Description: Variáveis de iteração de uma letra são usadas para objetos de domínio: `for t in tasks`, `for u in users`, `for c in categories`.
Impact: Reduz a legibilidade em blocos que já manipulam várias entidades relacionadas (task, user, category) no mesmo escopo.
Recommendation: Renomear para `task`, `user`, `category`, tornando o código autoexplicativo.

### [LOW] Imports Não Utilizados
File: app.py:7; routes/task_routes.py:7; routes/user_routes.py:6; routes/report_routes.py:8; utils/helpers.py:3-7
Description: `app.py` importa `os, sys, json` sem uso; `task_routes.py` importa `json, os, sys, time` sem uso; `user_routes.py` importa `hashlib, json` sem uso; `report_routes.py` importa `json` sem uso; `utils/helpers.py` importa `os, json, sys, math, hashlib` sem uso (apenas `re` é efetivamente usado).
Impact: Polui o namespace do módulo, confunde o leitor sobre as dependências reais do arquivo e mascara quais imports são de fato necessários.
Recommendation: Remover todos os imports não referenciados em cada arquivo, mantendo apenas o que é efetivamente utilizado.

================================
Total: 10 findings
================================
