## A. Análise Manual

###  Projeto: Code-smells-project:
*   **CRITICAL:**
    - Secret_key chumbadas no código gerando vulnerabilidade para o projeto. **Justificativa:** Gera vulnerabilidade para o projeto sendo assim facilitando a qualquer pessoa conseguir as credenciais tem fácil acesso ao projeto.
    **MEDIUM:**
    - Tratamento de erros duplicados, try/exception repetidos. **Justificativa:** Dificulta entendimento de cada erro, para caso necessário identificar um problema ou efetuar uma manutenção.
    - Mistura de responsabilidades nas classes. **Justificativa:** Em arquitetura de software é imprescindível que cada camada tenha sua e específica responsabilidade a fim de facilitar manutenção do código e testes unitários.
    **LOW:**
    - Magic strings/numbers chumbadas. **Justificativa:** Caso seja necessário alterar um dado que é utilizado em várias chamadas de funções da classe fica muito mais fácil a alteração em apenas uma variável ao invés de alterar em todos os pontos do código.
    - Utilização de prints ao invés de built-in com logs da linguagem. **Justificativa:** Logs da linguagem ferecem níveis de gravidade (como erro ou aviso), permitem redirecionar saídas para arquivos ou servidores facilmente.

###  Projeto: Ecommerce-api-legacy:
*   **CRITICAL:**
    - Secret_key chumbadas no código gerando vulnerabilidade para o projeto. **Justificativa:** Gera vulnerabilidade para o projeto sendo assim facilitando a qualquer pessoa conseguir as credenciais tem fácil acesso ao projeto.
    **HIGH:**
    - Invocação de método assíncrono de forma síncrona. **Justificativa:** Risco grande de gerar um travamento (Deadlocks) na aplicação além disso piora o desempenho da aplicação e esconde erros importantes que dificultam a correção de bugs.
    **MEDIUM:**
    - Mistura de responsabilidades nas classes. **Justificativa:** Em arquitetura de software é imprescindível que cada camada tenha sua e específica responsabilidade a fim de facilitar manutenção do código e testes unitários.
    **LOW:**
    - Nomenclatura de variáveis com apenas uma letra. **Justificativa:** Ilegibilidade de código, dificultando também a manutenção.
    - Imports não utilizados. **Justificativa:** Popuição no código, causando também lentidão na aplicação porque o sistema vai precisar ler o import que está chamando outra classe por exemplo.

  ###  Projeto: Task-manager-api:
*   **CRITICAL:**
    - Dados sensíveis chumbadas no código gerando vulnerabilidade para o projeto. **Justificativa:** Gera vulnerabilidade para o projeto sendo assim facilitando a qualquer pessoa conseguir as credenciais tem fácil acesso ao projeto.
    **MEDIUM:**
    - Tratamento de erros duplicados, try/exception repetidos. **Justificativa:** Dificulta entendimento de cada erro, para caso necessário identificar um problema ou efetuar uma manutenção.
    **MEDIUM:**
    - God Class, centralização de muitas responsabilidades nas classes. **Justificativa:** Em arquitetura de software é imprescindível que cada camada tenha sua e específica responsabilidade a fim de facilitar manutenção do código e testes unitários.
    **LOW:**
    - Magic strings/numbers chumbadas. **Justificativa:** Caso seja necessário alterar um dado que é utilizado em várias chamadas de funções da classe fica muito mais fácil a alteração em apenas uma variável ao invés de alterar em todos os pontos do código.
    - Imports não utilizados. **Justificativa:** Popuição no código, causando também lentidão na aplicação porque o sistema vai precisar ler o import que está chamando outra classe por exemplo.


---

## B. Construção da Skill

### Decisões de Design
*  Skill construída com base em técnicas avançadas de prompt engineering, como: Role Prompting, Few-shot learn, chain of thought e skeleton of thought. Role Prompting, Few-shot learn e chain of thought usei para criar a skill de orquestração definindo Persona e escopo, few-shot com exemplos de acionamento dos arquivos de referência e chain of thought com a técnica `<thinking>` forçando assim o agente a raciocinar passo a passo antes de executar todas as fases garantindo que o agente não pule nenhuma fase. Para a skill de auditoria utilizei a técnica Skeleton of Thought com `<thinking>` forçando também o agente a criar um esqueleto mental antes de gerar o relatório final. Para a skill de refactor do projeto utilizei as técnicas Chain of Thought com  `<thinking>` forçando assim o agente a raciocinar passo a passo antes de modificar as pastas e arquivos para garantir que não haja nenhuma duplicidade de arquivos e que as dependências sejam inseridas nos arquivos corretos.

### Seleção de Anti-patterns

Anti-patterns incluídos com base 
Priorizamos a inclusão dos anti-patterns catalogados na Seção A porque eles representam as três frentes principais da engenharia moderna:
*   **Segurança:** (Vazamento de Dados) - Protege o negócio.
*   **Escalabilidade:** (N+1 e Transações) - Protege a infraestrutura.
*   **Manutenibilidade:** (Logging e Dead Code) - Protege a saúde mental do time.

### Agnosticismo de Tecnologia
A skill foi projetada para ser **agnóstica de linguagem**. 
*   **Como garanti isso:** Na construção da skill estou passando ao modelo vários exemplos genéricos de códigos de linguagens diferentes garantiando assim que não é para ele se basear em apenas uma linguagem de programação. 

### Desafios Encontrados
  - Na primeira iteração o modelo gerou várias pastas e arquivos duplicados, gerando vários conflitos no start da aplicação, tive que alterar novamente a SKILL adicionando instruções mais claras e técnica de CoT, para que isso seja evitado.
  - Identificação de todos os anti-patterns de cada projeto, para depois escreve-los nos arquivos de referência pensando nas melhores técnicas de prompt engineer para que o modelo execute as tarefas com precisão.

---

## C. Resultados

### 1. Resumo dos Relatórios de Auditoria

================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python 3 + Flask 3.1.1 (flask-cors 5.0.1), SQLite (sqlite3 stdlib)
Files:   4 analyzed | ~780 estimated lines of code

## Summary
CRITICAL: 4 | HIGH: 2 | MEDIUM: 3 | LOW: 4

---

Resumo
================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   Node.js + Express.js (sqlite3)
Files:   3 analyzed | ~150 estimated lines of code

## Summary
CRITICAL: 2 | HIGH: 3 | MEDIUM: 3 | LOW: 2

### 2. Comparação Antes/Depois
**Project: code-smells-project**
Estrutura de pastas antes do refactor:
![alt text](<Pasted Graphic 14.png>)

Estrutura de pastas depois do refactor:
![alt text](image.png)

---

**Project: ecommerce-api-legacy**
## Antes e Depois

| Antes do refactor | Depois do refactor |
|:---:|:---:|
| <img src="![alt text](<JS app.js.png>)" width="400"> | <img src="![alt text](<Pasted Graphic 21.png>)" width="400"> |

### 3. Checklist de validação preenchido

**Project: code-smells-project**
## Validação:
- `venv/bin/python -c "import app"` — importação limpa.
- Boot real (`venv/bin/python app.py`) — subiu sem erros em http://localhost:5050, log estruturado confirmando inicialização do banco.
- Testado via curl: GET /, /health, /produtos/1, /produtos/9999 (404), /usuarios; POST /login (sucesso e falha), /pedidos; GET /pedidos, /relatorios/vendas; POST /admin/query (404, confirmando remoção); POST /admin/reset-db — todos responderam com status/payload esperados.
- Confirmado nos logs: notificações e reset de admin passam por `logging`, não `print`.
- Ambiente de teste limpo após validação (loja.db e log temporário removidos).

---
**Project: ecommerce-api-legacy**
## Validação:
- `npm install` → 1 pacote novo (bcryptjs) instalado com sucesso, sem erros de build.
- `npm start` → boot limpo, log: "Banco de dados inicializado com sucesso." + "Frankenstein LMS rodando e pronto na porta 3000...".
- Requisições de `api.http` testadas via curl, mesmos endpoints/portas/payloads da versão original:
  - POST /api/checkout (novo usuário, cartão Visa) → 200 {"msg":"Sucesso","enrollment_id":2}
  - POST /api/checkout (cartão não-Visa) → 400 "Pagamento recusado"
  - POST /api/checkout (payload incompleto) → 400 "Bad Request"
  - POST /api/checkout (curso inexistente) → 404 "Curso não encontrado"
  - GET /api/admin/financial-report → 200, valores agregados corretos (via JOIN, sem N+1)
  - DELETE /api/users/1 → 200 "Usuário deletado, mas as matrículas e pagamentos ficaram sujos no banco."
  - GET /api/admin/financial-report (após delete) → "Unknown" corretamente reportado para matrícula órfã, sem crash
- Nenhuma regressão de contrato externo (mesmas rotas, mesmos status codes, mesmos formatos de payload).


### 4. Screenshots ou logs das aplicações rodando após refatoração.

**Project: code-smells-project**
![alt text](<Pasted Graphic 18.png>)
---
**Project: ecommerce-api-legacy**
![alt text](<Pasted Graphic 23.png>)

## D. Como executar

**Pré-requisitos:**
- instale as dependências de cada projeto, exemplo:
- code-smells-project e task-manager-api:
python3 -m venv venv (instalar o ambiente virtual isolado para o projeto)
source venv/bin/activate
pip install -r requirements.txt
pip freeze > requirements.txt
python3 app.py

- ecommerce-api-legacy:
instalar node
npm install
npm run dev

**Comandos para executar a Skill em cada projeto:**
**via Claude CLI:**
/refactor-arch analise e refatore o projeto code-smells-project
/refactor-arch analise e refatore o projeto ecommerce-api-legacy
/refactor-arch analise e refatore o projeto task-manager-api

**Como validar o funcionamento:**
