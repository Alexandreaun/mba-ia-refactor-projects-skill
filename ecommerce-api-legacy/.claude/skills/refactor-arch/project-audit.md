## Fase 2 - Auditoria do Projeto

<Instructions>
Inspecione o código-fonte comparando-o com o catálogo de anti-patterns abaixo. O objetivo é encontrar **no mínimo 5 problemas**, incluindo obrigatoriamente pelo menos um de nível **CRITICAL** ou **HIGH**, dois de nível **MEDIUM** e dois de nível **LOW**. Baseie suas sugestões de correção no **Playbook de Transformações**.

**Metodologia de Execução (Skeleton of Thought):**
Antes de gerar e salvar o relatório final, você DEVE obrigatoriamente estruturar o seu raciocínio passo a passo utilizando uma tag `<thinking>` no terminal (esta tag não deve ir para o arquivo final). Siga estes passos internamente:
1. **Skeleton (Rascunho):** Mapeie rapidamente todos os arquivos do projeto e crie uma lista concisa dos candidatos a anti-patterns encontrados (formato: `[Severidade] Anti-pattern - Arquivo:Linha`).
2. **Constraint Check (Validação):** Verifique se o seu esqueleto contém exatamente/no mínimo a cota exigida (1 Critical/High, 2 Medium, 2 Low). Se faltar algum, busque novamente no código antes de avançar.
3. **Flesh Out (Expansão):** Apenas após validar o esqueleto, expanda cada item utilizando as definições do Catálogo e as recomendações do Playbook.
4. **Action (Ação):** Salve o resultado final no arquivo conforme as instruções de Saída.

**Regras de Auditoria:**
1. **Precisão Absoluta:** Para cada ocorrência, registre o arquivo exato e o intervalo de linhas. É estritamente proibido usar termos vagos como "em algum lugar neste arquivo".
2. **Sem Subjetividade:** Não opine sobre a gravidade da vulnerabilidade; classifique-a puramente de acordo com as definições do Catálogo abaixo.
3. **Verificação de Obsolescência:** Verifique explicitamente APIs obsoletas ou inseguras para a versão da pilha/framework detectada (ex: padrões ORM desatualizados, hashes inseguros) e recomende o equivalente moderno.

---

### Catálogo de Anti-Patterns e Severidades

**CRITICAL**
1. **Hardcoded Secrets & Configs:** Chaves de API, senhas, tokens ou URLs de banco de dados escritos diretamente no código-fonte em vez de variáveis de ambiente.
2. **God Class / Monolithic Entrypoint:** Um único arquivo ou classe que mistura roteamento (ou UI), regras de negócio complexas e consultas diretas ao banco de dados ou APIs externas.

**HIGH**
3. **Fat Controllers / Logic in View:** Controladores ou Componentes Visuais que contêm regras de negócio puras, cálculos complexos ou manipulação direta de dados, impedindo o teste unitário da regra sem carregar a interface/rede.
4. **Tight Coupling (Forte Acoplamento):** Instanciação direta de dependências complexas (bancos de dados, serviços externos) dentro da classe consumidora, inviabilizando injeção de dependência (DI) e mocks.
5. **Sync over Async:** Invocação de métodos assíncrono de forma síncrona. (ex: manager.initDb())

**MEDIUM**
6. **N+1 Query Problem / Inefficient Loops:** Consultas a banco de dados ou chamadas de rede feitas dentro de loops de iteração, em vez de buscar os dados em lote (batch/JOINs).
7. **Swallowed Exceptions / Duplicated Error Handling:** Blocos `try/catch` que ignoram o erro silenciosamente ou tratamento de erro descentralizado e repetido em cada função, sem um handler global.
8. **Deprecated/Unsafe APIs:** Uso de bibliotecas abandonadas, funções reprovadas na versão atual do framework ou algoritmos criptográficos inseguros (ex: MD5, SHA1).

**LOW**
9. **Magic Numbers / Magic Strings:** Uso de valores literais soltos no código (ex: `if (status == 2)`, `setTimeout(fn, 86400000)`) sem atribuição a constantes semânticas.
10. **Nomenclatura de Variáveis inconsistentes:** Nomear variáveis com apenas uma letra (ex: let u = req.body.usr; let e = req.body.eml;)
11. **Imports desnecessários:** Imports não utilizados poluindo o código.

---

### Playbook de Transformação (Antes / Depois)
Use estes padrões para preencher o campo `Recommendation` no seu relatório. Adapte a sintaxe à linguagem do projeto atual.

**1. Hardcoded Secrets (CRITICAL)**
*   *Antes:* `db_connect("postgres://admin:1234@localhost/db")`
*   *Depois:* `db_connect(ENV['DATABASE_URL'])`

**2. God Class (CRITICAL)**
*   *Antes:* A rota `/users` valida o request, faz o `SELECT` no SQL, formata os dados e retorna o JSON, tudo no mesmo bloco.
*   *Depois:* A rota chama `UserController`, que repassa os dados para o `UserService` (negócio), que busca os dados no `UserRepository` (dados).

**3. Fat Controllers / Logic in View (HIGH)**
*   *Antes:* `Controller: if (user.age > 18 && user.credit > 500) { applyDiscount() }`
*   *Depois:* `Controller: discountService.applyIfEligible(user)`. A regra mora no Service/Model.

**4. Tight Coupling (HIGH)**
*   *Antes:* `class Payment { init() { this.api = new StripeAPI() } }`
*   *Depois:* `class Payment { init(api: PaymentGateway) { this.api = api } }`. A dependência é injetada.

**5. Sync over Async (HIGH)**
*   *Antes:* Chamando manager.initDb(); de forma síncrona
    ```tsx
    const app = express();
    app.use(express.json());

    const manager = new AppManager();
    manager.initDb();
    manager.setupRoutes(app);
    ```

*   *Depois:* Chamando manager.initDb(); de forma assíncrona
    ```tsx
    async function bootstrap() {
    try {
        const app = express();
        app.use(express.json());

        const manager = new AppManager();
        
        await manager.initDb(); 
        logger.info("Banco de dados inicializado com sucesso.");

        manager.setupRoutes(app);

        app.listen(config.port, () => {
            logger.info(`Frankenstein LMS rodando e pronto na porta ${config.port}...`);
        });

        } catch (error) {
        logger.fatal({ err: error }, "Falha crítica ao iniciar a aplicação");
        process.exit(1); 
        }
    }
    ```

**6. N+1 Queries (MEDIUM)**
*   *Antes:* `for user in users: get_posts_for_user(user.id)` (100 consultas).
*   *Depois:* `get_posts_for_users(user_ids)` (1 consulta com IN clause / Eager Loading).

**7. Swallowed Exceptions (MEDIUM)**
*   *Antes:* `try { doRiskThing() } catch (e) { print(e) }`
*   *Depois:* A rota lança o erro nativamente e um `GlobalErrorHandler` (middleware/interceptor) captura, loga e formata a resposta padronizada para o cliente.

**8. Deprecated / Unsafe APIs (MEDIUM)**
*   *Antes:* `hash_password(input, algorithm: "MD5")`
*   *Depois:* `hash_password(input, algorithm: "bcrypt" / "Argon2")`

**9. Magic Numbers (LOW)**
*   *Antes:* `if (password.length < 8)`
*   *Depois:* `const MIN_PASSWORD_LENGTH = 8; if (password.length < MIN_PASSWORD_LENGTH)`

**10. Nomenclatura de Variáveis inconsistentes (LOW)**
*   *Antes:* `let u = req.body.usr;`
*   *Depois:* `let user = req.body.usr`

**11. Imports não utilizados (LOW)**
*   *Antes:* `from flask import jsonify`
*   *Depois:* ``

</Instructions>

<Outputs>
Não imprima o relatório inteiro no terminal. Em vez disso:

1. Verifique se o diretório `reports/` existe na raiz do projeto. Se não, crie-o.
2. Validação de Contexto: Antes de salvar, verifique na pasta `reports/` se já existe um relatório prévio referente ao código/módulo que você está auditando agora.
3. Se já existir (Sobrescrita): Sobrescreva o arquivo existente (ex: substituindo o conteúdo do antigo `reports/audit-project-1.md`). NUNCA crie um arquivo duplicado se a auditoria for do mesmo contexto.
4. Se for um contexto inédito (Criação): Crie um arquivo novo utilizando um índice numérico sequencial e incremental, seguindo o padrão audit-project-{numero_sequencial}.md (ex: `reports/audit-project-1.md`, `reports/audit-project-2.md`, e assim por diante).
5. O conteúdo do arquivo DEVE utilizar EXATAMENTE a estrutura abaixo (Ordene os achados como CRITICAL → HIGH → MEDIUM → LOW):

<Template_Relatorio>
```text
================================
ARCHITECTURE AUDIT REPORT
================================
```
Stack:   <language + framework>
Files:   <N> analyzed | ~<LOC> estimated lines of code

## Summary
CRITICAL: <n> | HIGH: <n> | MEDIUM: <n> | LOW: <n>

## Findings

### [<SEVERITY>] <Anti-pattern name>
File: <path>:<line-or-range>
Description: <what is wrong, concretely>
Impact: <why it matters — testability, security, correctness, maintainability>
Recommendation: <the fix, in one or two sentences based on the Playbook>

... (one block per finding)

================================
Total: <n> findings
================================
</Template_Relatorio>
</Outputs>

<Execution_Flow>
**DIRETIVA DE PARADA (HALT):**
Após criar e salvar o arquivo de relatório com sucesso, o agente **não deve exibir o relatório inteiro no terminal**. Em vez disso, a única resposta visível no chat/terminal deve ser:
1. Uma linha confirmando a gravação (ex: `[OK] Relatório salvo em reports/audit-project-1.md`).
2. A pergunta de controle explícita: **"Prosseguir com a refatoração (Fase 3)? [s/n]"**
3. **NÃO modifique, crie, mova ou exclua** nenhum outro arquivo do projeto até que o usuário responda.
</Execution_Flow>