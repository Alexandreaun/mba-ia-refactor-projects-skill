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
*  Skill construida com base em técnicas avançadas de prompt engineer, como: Role Prompting, Few-shot learn e chain of thought.

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
  - Na primeira iteração o modelo gerou várias pastas e arquivos duplicados, gerando vários conflitos no start da aplicação, tive que alterar novamente a SKILL adicionando instruções mais claras para que isso seja evitado.
  - Identificação de todos os anti-patterns de cada projeto, para depois escreve-los nos arquivos de referência pensando nas melhores técnicas de prompt engineer para que o modelo execute as tarefas com precisão.

---

## C. Resultados

### 1. Resumo dos Relatórios de Auditoria


### 2. Comparação Antes/Depois (Exemplo)


### 3. Checklist de validação preenchido


### 4. Screenshots ou logs das aplicações rodando após refatoração.


## D. Como executar

**via Claude CLI:**
/refactor-arch analise e refatore o projeto code-smells-project

**via Terminal:**
cd code-smells-project && claude -p "/refactor-arch analise e refatore o projeto code-smells-project"