## Fase 3 - Refatoração para MVC e Validação

<Instructions>
**Diretivas de Execução:**
O usuário autorizou a refatoração. Sua tarefa agora é reestruturar fisicamente a base de código do projeto adotando os princípios da arquitetura MVC (Model-View-Controller) ou equivalente, aplicando as melhorias exigidas pelo relatório da Fase 2.

**Ancoragem Tecnológica (Ponte com a Fase 1):**
Utilize estritamente a **Linguagem, Framework e Dependências** identificados no relatório da Fase 1. O código refatorado deve ser 100% idiomático, respeitando as convenções de nomenclatura, gerenciamento de pacotes, estilos de importação e padrões arquiteturais nativos da tecnologia específica do projeto.

**Autorização de Sistema de Arquivos e Terminal:**
Você tem permissão total para criar diretórios, mover arquivos, deletar códigos obsoletos e executar comandos de terminal no projeto para validação de integridade.

**Metodologia de Refatoração (Chain of Thought):**
ANTES de modificar, criar ou mover qualquer arquivo, você DEVE utilizar a tag `<thinking>` para realizar o raciocínio lógico e planejamento da execução passo a passo:
1. **Mapeamento de Destino:** Defina exatamente quais blocos de código irão para `/models`, `/controllers`, `/views`, `/config` ou `/services`.
2. **Grafo de Dependências:** Identifique todos os arquivos que importam os módulos modificados. Planeje a atualização das rotas de importação (ex: atualizar de `import { x } from './utils'` para `import { x } from '../config/utils'`).
3. **Estratégia In-Place:** Confirme quais arquivos já existem e serão apenas reescritos.

### Playbook de Refatoração (Padrões de Transformação)
Ao resolver os itens do relatório `audit-project-{numero}.md`, aplique as transformações abaixo adaptadas para a sintaxe da linguagem detectada na Fase 1:

1. **Hardcoded Secrets:**
   * *Ação:* Crie um arquivo de configuração (ex: `.env`, `.xcconfig` ou módulo de `Config`). Substitua credenciais, tokens e URLs de banco de dados soltos no código por chamadas de variáveis de ambiente.
2. **God Class / Monolithic Entrypoint:**
   * *Ação:* Quebre o arquivo gigante. O Entrypoint deve conter apenas o setup (inicialização de ambiente, conexão com banco e carregamento de rotas/telas). Mova as regras de negócio e persistência para a camada /models e a orquestração de fluxo para /controllers.
3. **Fat Controllers / Logic in View:**
   * *Ação:* Se uma View (componente visual ou formatador de resposta) ou um Controller realiza regras de domínio ou processamento pesado, extraia essa lógica estritamente para a camada /models. O Controller deve apenas receber a entrada, acionar o Model e repassar o resultado para a View.
4. **Tight Coupling (Forte Acoplamento):**
   * *Ação:* Refatore instâncias diretas de dependências complexas. Altere o construtor/inicializador das classes para receber a dependência como parâmetro (Injeção de Dependência).
5. **N+1 Queries / Inefficient Loops:**
   * *Ação:* Reescreva laços de repetição que fazem consultas repetidas. Faça chamadas em lote ou utilize Eager Loading compatível com o ORM detectado.
6. **Swallowed Exceptions:**
   * *Ação:* Remova blocos de captura de erro vazios ou que apenas logam no console. Lance a exceção nativamente e crie um Manipulador de Erros Global adequado ao framework.
7. **Deprecated APIs:**
   * *Ação:* Atualize assinaturas de métodos defasados ou substitua bibliotecas obsoletas pelas recomendações atuais da linguagem.
8. **Magic Numbers:**
   * *Ação:* Extraia valores literais não documentados para constantes semânticas globais ou no topo do arquivo.
9. **Improper Output Routing:**
   * *Ação:* Ao invés de escrever print(""), utilize o módulo built-in de log da linguagem de programação correspondente ao projeto.
10. **Premature Server Binding:**
   * *Ação:* Ao chamar funções assíncronas utilize async/await.
11. **Nomenclatura de Variáveis inconsistentes:**
   * *Ação:* Nomeie as variáveis de acordo com os dados que elas a carregam para facilitar a legibilidade.
12. **Imports não utilizados:**
   * *Ação:* Caso um framework não esteja sendo utilizado na classe remova o import.

---

**Passo a Passo da Refatoração:**

1. **Setup da Estrutura:** 
Instancie os diretórios da nova arquitetura na raiz do projeto (ex: `/models`, `/controllers`, `/views`, `/config`, `/services`).

  ⚠️ REGRAS DE ARQUIVOS (APLIQUE ESTRITAMENTE):
  **Checagem Prévia:** Antes de criar qualquer pasta ou arquivo, verifique se ele já existe na árvore de diretórios.
  **Proibição de Duplicatas:** NUNCA crie arquivos/pastas com nomes alternativos (como controller2.py, models_novo ou anexando _refactored).
  **Mutação In-Place:** Se o arquivo ou diretório destino já existir, você OBRIGATORIAMENTE deve reaproveitá-lo. Aplique as alterações e refatorações reescrevendo o código diretamente dentro do arquivo original (in-place).

2. **Configuração e Ambiente:** Isole configurações sensíveis usando o Padrão 1 do Playbook.
3. **Models (Camada de Dados):** Mova toda a responsabilidade de acesso a dados e persistência para esta camada.
4. **Controllers (Regras de Negócio e Orquestração):** Extraia a lógica de aplicação para mediadores (Padrão 3 e 4). Também considere o padrão 9 para melhorias no código com relação a Improper Output Routing.
5. **Views / Routes (Camada de Apresentação):** Limpe os arquivos de interface externa para que APENAS formatem entradas e saídas (JSON ou renderização visual).
6. **Tratamento de Erros:** Centralize a captura de exceções (Padrão 6).
7. **Entrypoint:** Limpe o ponto de entrada principal (Padrão 2).
8. **Correção de Imports:** Verifique e atualize **TODOS** os caminhos de importação nos arquivos afetados.
9. **Validação e Auto-Cura (Boot & Check):** Após finalizar as alterações, execute o comando de compilação ou inicialização no terminal compatível com a linguagem da Fase 1 (ex: `npm run build`, `python app.py`, ou `docker-compose up`). **Regra de Auto-Cura:** Se o comando falhar (ex: `ModuleNotFoundError`, erro de sintaxe), você OBRIGATORIAMENTE deve ler o log de erro, corrigir o problema de importação/sintaxe e rodar o comando novamente. Repita até que o build/boot seja concluído com sucesso.

**Regras de Comportamento (Contrato):**
- A refatoração é estritamente estrutural. O comportamento externo (fluxos de UI, caminhos de URL, payloads) NÃO pode ser alterado, salvo na resolução de vulnerabilidade crítica com aviso explícito.
</Instructions>

<Examples>

## Exemplos Práticos

### 💡 Diretrizes de Código
  
  * **❌ Código Legado Improper Output Routing
```python
try:
    process_payment()
except Exception as e:
    print(f"Erro ao processar pagamento: {e}")
```
* **✅ Código Limpo e Refatorado - Utilizando logger.error
```python
import logging
logger = logging.getLogger(__name__)
try:
    process_payment()
except Exception as e:
    logger.error("Erro ao processar pagamento: %s", e)
```

  * **❌ Código Legado Improper Output Routing
```java
try {
    processPayment();
} catch (Exception e) {
    System.out.println("Erro ao processar pagamento: " + e.getMessage());
}
```
* **✅ Código Limpo e Refatorado - O logger.error() permite que a aplicação encaminhe o erro para o sistema de logs configurado, em vez de simplesmente escrever no stdout.
```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
private static final Logger logger = LoggerFactory.getLogger(PaymentService.class);
try {
    processPayment();
} catch (Exception e) {
    logger.error("Erro ao processar pagamento", e);
}
```

  * **❌ Código Legado Improper Output Routing
```javascript
try {
    processPayment();
} catch (error) {
    console.log("Erro ao processar pagamento:", error);
}
```
* **✅ Código Limpo e Refatorado - Considerando um logger como o Pino ou Winston, a aplicação consegue estruturar e encaminhar o erro adequadamente.
```javascript
try {
    processPayment();
} catch (error) {
    logger.error("Erro ao processar pagamento", {
        error: error.message,
        stack: error.stack
    });
}
```

### 💡 Diretrizes de Arquitetura e Código 
Ao gerar e modificar o código, você DEVE aplicar a separação rigorosa de responsabilidades. NUNCA misture regras de negócio com detalhes de infraestrutura (como rotas HTTP ou renderização visual). Observe os exemplos abaixo de como transformar código legado em arquitetura limpa (SOLID):

**Exemplo 1: Separação de Camadas (Web Backend)**

* **❌ Código Legado (God Controller):** Rota, negócio e banco de dados no mesmo arquivo.
```typescript
// routes.ts (RUIM)
app.post('/users', async (req, res) => {
  if (!req.body.email) return res.status(400).send("Email obrigatório");
  
  // Regra de negócio e infraestrutura misturadas
  const hashedPassword = crypto.createHash('sha256').update(req.body.password).digest('hex');
  
  // Acesso direto a dados no meio da rota HTTP
  await db.query('INSERT INTO users (email, password) VALUES ($1, $2)', [req.body.email, hashedPassword]);
  
  res.status(201).send("Criado");
});
```

* **✅ Código Limpo e Refatorado (Padrão MVC):**
```typescript
// 1. MODEL (Camada de Dados e Regras de Negócio Puras)
// UserModel.ts
export class UserModel {
  static async create(email: string, passwordPlain: string): Promise<any> {
    if (!email) throw new Error("Email obrigatório");
    
    const hashedPassword = crypto.createHash('sha256').update(passwordPlain).digest('hex');
    const result = await db.query(
      'INSERT INTO users (email, password) VALUES ($1, $2) RETURNING *', 
      [email, hashedPassword]
    );
    return result.rows[0];
  }
}

// 2. CONTROLLER (Orquestração de I/O HTTP)
// UserController.ts
import { UserModel } from './UserModel';

export class UserController {
  static async createUser(req: Request, res: Response) {
    try {
      const { email, password } = req.body;
      const user = await UserModel.create(email, password);
      // Delega a apresentação para a View (neste caso, o formatador JSON)
      return UserView.renderSuccess(res, user);
    } catch (e) {
      return UserView.renderError(res, e.message);
    }
  }
}

// 3. VIEW / ROUTES (Apresentação, Formatação e Roteamento)
// UserView.ts (Formata a saída da API)
export class UserView {
  static renderSuccess(res: Response, user: any) {
    return res.status(201).json({ success: true, data: { id: user.id, email: user.email } });
  }
  static renderError(res: Response, message: string) {
    return res.status(400).json({ success: false, error: message });
  }
}
// routes.ts (Mapeia a requisição para o Controller)
app.post('/users', UserController.createUser);
```

**Exemplo 2: Separação de Responsabilidades (Web Frontend)**

* **❌ Código Legado (Fat Component):** UI renderiza, faz requisições HTTP diretas e possui regras lógicas complexas.
```tsx
// Dashboard.tsx (RUIM)
export function Dashboard() {
  const [metrics, setMetrics] = useState([]);

  useEffect(() => {
    // Chamada de API direta no componente visual
    fetch('[https://api.site.com/metrics](https://api.site.com/metrics)')
      .then(res => res.json())
      .then(data => {
        // Regra de negócio/Filtro presa na renderização
        const activeMetrics = data.filter(item => item.isActive && item.value > 100);
        setMetrics(activeMetrics);
      });
  }, []);

  return <div>{metrics.map(m => <span key={m.id}>{m.name}</span>)}</div>;
}
```

* **✅ Código Limpo e Refatorado (Padrão MVC no Frontend):**
```tsx
// 1. MODEL (Lida puramente com a Rede, API e Regras de Negócio/Filtros)
// DashboardModel.ts
export const DashboardModel = {
  async getActiveMetrics() {
    const response = await fetch('[https://api.site.com/metrics](https://api.site.com/metrics)');
    const data = await response.json();
    // A regra de negócio pertence ao Model
    return data.filter(item => item.isActive && item.value > 100);
  }
};

// 2. CONTROLLER (Container Component: Lida com Estado, Ciclo de Vida e Orquestração)
// DashboardController.tsx
import { DashboardModel } from './DashboardModel';
import { DashboardView } from './DashboardView';

export function DashboardController() {
  const [metrics, setMetrics] = useState([]);
  
  useEffect(() => {
    // O Controller pede os dados ao Model e atualiza o estado
    DashboardModel.getActiveMetrics().then(setMetrics);
  }, []);
  
  // O Controller injeta os dados na View
  return <DashboardView metrics="{metrics}"/>;
}

// 3. VIEW (Presentational Component: Componente passivo, estritamente visual)
// DashboardView.tsx
export function DashboardView({ metrics }) {
  // A View não sabe de onde vêm os dados nem aplica regras lógicas, apenas renderiza HTML/CSS
  return (
    <div>
      {metrics.map(m => (
        <span key={m.id}>{m.name}</span>
      ))}
    </div>
  );
}
```
</Examples>

<Execution_Flow>
1. Realize o planejamento na tag `<thinking>`.
2. Refatore o código reescrevendo in-place e movendo as responsabilidades.
3. Atualize TODOS os *imports* afetados.
4. Execute a validação (Boot & Check) e aplique a auto-cura caso encontre erros.
5. Apenas após garantir que o projeto roda sem quebrar, imprima a Saída.
</Execution_Flow>

<Outputs>
**Formato de Saída Obrigatório:**
Após compilar/validar com sucesso, imprima no terminal:

```text
================================
PHASE 3: REFACTORING COMPLETE
================================
## New Project Structure
<imprima a árvore de diretórios e arquivos do novo layout (tree)>

## Resolvidas:
- <cite as correções realizadas baseadas no relatório da Fase 2>

## Validação:
- <cite o comando executado e o resultado do boot/compilação>
================================
```
</Outputs>