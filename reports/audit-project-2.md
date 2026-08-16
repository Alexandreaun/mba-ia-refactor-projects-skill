================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   Node.js + Express.js (sqlite3)
Files:   3 analyzed | ~150 estimated lines of code

## Summary
CRITICAL: 2 | HIGH: 3 | MEDIUM: 3 | LOW: 2

## Findings

### [CRITICAL] Hardcoded Secrets & Configs
File: src/utils.js:2-5
Description: `dbUser`, `dbPass`, `paymentGatewayKey` e `smtpUser` estão escritos em texto plano diretamente no objeto `config`, incluindo uma chave de gateway de pagamento com prefixo `pk_live_`.
Impact: Qualquer pessoa com acesso ao repositório obtém credenciais de produção e a chave de pagamento; vazamento do código-fonte compromete diretamente sistemas externos (banco de dados e gateway financeiro).
Recommendation: Mover todos os valores para variáveis de ambiente (`process.env.DB_PASS`, `process.env.PAYMENT_GATEWAY_KEY`, etc.), carregadas via `.env` (dotenv) e nunca commitadas.

### [CRITICAL] God Class / Monolithic Entrypoint
File: src/AppManager.js:4-141
Description: A classe `AppManager` concentra em um único arquivo a conexão com o banco (`this.db`), a criação de schema/seed (`initDb`), a definição de todas as rotas (`setupRoutes`) e toda a lógica de negócio de checkout, matrícula, pagamento e relatório financeiro.
Impact: Impede testes unitários isolados, dificulta manutenção e viola Single Responsibility — qualquer mudança de rota, regra de negócio ou schema exige editar a mesma classe.
Recommendation: Separar em camadas MVC: `models/` (acesso a dados por entidade), `controllers/` (orquestração de request/response) e `services/` (regras de negócio de checkout e relatório), com `AppManager`/`app.js` apenas fazendo o wiring.

### [HIGH] Fat Controller / Logic in Route Handler
File: src/AppManager.js:28-78
Description: O handler da rota `POST /api/checkout` executa validação de payload, consulta de curso, consulta/criação de usuário, hashing de senha, "processamento" de pagamento (`cc.startsWith("4")`) e gravação de matrícula/pagamento/log de auditoria, tudo dentro do callback da rota.
Impact: Regra de negócio crítica (checkout financeiro) não pode ser testada sem subir o servidor HTTP; qualquer alteração na regra de pagamento arrisca quebrar o parsing de request junto.
Recommendation: Extrair a lógica para um `CheckoutService.process(input)`, deixando o controller apenas validar entrada, chamar o service e formatar a resposta.

### [HIGH] Tight Coupling (Forte Acoplamento)
File: src/AppManager.js:7
Description: `this.db = new sqlite3.Database(':memory:')` instancia a dependência de banco diretamente dentro do construtor da classe que também contém a lógica de negócio.
Impact: Impossibilita injeção de um banco de teste/mock, acoplando `AppManager` permanentemente ao driver `sqlite3` e ao modo `:memory:`.
Recommendation: Injetar a conexão de banco via construtor (`constructor(db) { this.db = db }`), permitindo passar uma instância real ou um mock nos testes.

### [HIGH] Premature Server Binding
File: src/app.js:8-10
Description: `manager.initDb()` é chamado de forma síncrona (sem `await`/callback de conclusão) e imediatamente seguido por `manager.setupRoutes(app)` e `app.listen(...)`, mesmo `initDb` disparando `CREATE TABLE`/`INSERT` assíncronos via `db.serialize`.
Impact: O servidor pode aceitar requisições antes que as tabelas/seeds tenham sido de fato criadas, causando falhas intermitentes em boot a frio.
Recommendation: Tornar `initDb` retornar uma Promise (envolvendo os callbacks do sqlite3) e usar `async function bootstrap() { await manager.initDb(); ...; app.listen(...) }`, com tratamento de erro fatal no boot.

### [MEDIUM] N+1 Query Problem
File: src/AppManager.js:80-129
Description: A rota `/api/admin/financial-report` itera cursos (`courses.forEach`) e, para cada um, consulta matrículas; para cada matrícula, faz mais duas consultas (`users`, `payments`) dentro do loop — gerando O(cursos × matrículas × 2) queries.
Impact: Com poucos dezenas de cursos/matrículas, o relatório já gera dezenas a centenas de round-trips ao banco, degradando performance e aumentando risco de condição de corrida no acumulador `coursesPending`/`enrPending`.
Recommendation: Substituir por consultas em lote com `JOIN` (ex: `SELECT c.title, e.id, u.name, p.amount, p.status FROM courses c LEFT JOIN enrollments e ON ... LEFT JOIN users u ON ... LEFT JOIN payments p ON ...`) e agregar os resultados em memória em uma única passada.

### [MEDIUM] Swallowed Exceptions / Erro Descentralizado
File: src/AppManager.js:92,131-137
Description: Em `db.all("SELECT * FROM enrollments...", [], (err, enrollments) => {...})` (linha 92) o `err` é recebido mas nunca verificado antes de usar `enrollments`; na rota `DELETE /api/users/:id` (linhas 133-136) o `err` do `db.run` também é ignorado e a resposta de sucesso é enviada incondicionalmente. Cada rota do arquivo repete seu próprio tratamento de erro ad-hoc em vez de um handler central.
Impact: Erros de banco silenciados geram respostas de sucesso falsas ao cliente e tornam debugging difícil; a duplicação de tratamento de erro por rota aumenta a chance de inconsistência.
Recommendation: Checar `err` em todo callback e repassar via `next(err)`; centralizar formatação de erro em um middleware `app.use((err, req, res, next) => {...})` do Express.

### [MEDIUM] Deprecated/Unsafe API — Hashing Inseguro
File: src/utils.js:17-23 (uso em src/AppManager.js:68)
Description: `badCrypto` implementa um "hash" caseiro concatenando substrings de Base64 da senha em um laço de 10000 iterações e truncando o resultado — não é um algoritmo criptográfico reconhecido e é trivialmente reversível/colidível.
Impact: Senhas de usuário ficam praticamente em texto plano; qualquer vazamento do banco expõe credenciais dos usuários sem proteção real.
Recommendation: Substituir por `bcrypt` ou `argon2` (`await bcrypt.hash(senha, 12)`), armazenando apenas o hash com salt gerado pela biblioteca.

### [LOW] Magic Strings
File: src/AppManager.js:46-48
Description: A validação de pagamento usa o literal mágico `cc.startsWith("4")` para decidir aprovação, e os status `"PAID"`/`"DENIED"` são strings soltas repetidas em várias partes do arquivo (linhas 46, 48, 54, 108) sem constante central.
Impact: Qualquer alteração na regra de aprovação exige buscar e trocar literais espalhados, sujeito a erro de digitação e inconsistência entre rotas.
Recommendation: Extrair para constantes nomeadas, ex.: `const PAYMENT_STATUS = { PAID: 'PAID', DENIED: 'DENIED' }` e `const VISA_PREFIX = '4'`.

### [LOW] Nomenclatura de Variáveis Inconsistente
File: src/AppManager.js:29-33
Description: O handler de checkout usa nomes de uma letra para variáveis de domínio: `let u = req.body.usr; let e = req.body.eml; let p = req.body.pwd; let cid = req.body.c_id; let cc = req.body.card;`.
Impact: Reduz legibilidade e aumenta o custo cognitivo de revisão/manutenção do fluxo financeiro mais crítico da aplicação.
Recommendation: Renomear para nomes descritivos: `userName`, `email`, `password`, `courseId`, `cardNumber`.

================================
Total: 10 findings
================================
