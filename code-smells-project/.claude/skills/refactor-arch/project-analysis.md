## Fase 1 - Análise do Projeto

**Diretivas:**
Nesta fase, você deve escanear a base de código fornecida e extrair o contexto macro do projeto. Para garantir alta precisão, aplique as seguintes restrições:

- **Language & Framework:** Deduza a partir de arquivos de manifesto (como `requirements.txt`, `package.json`, `Package.swift`, `pyproject.toml`, etc.) e das declarações de importação. Não adivinhe baseando-se apenas nas extensões dos arquivos.
- **Dependencies:** Liste APENAS as dependências *core* que impactam a arquitetura (ex: ORMs, bibliotecas de processamento/IA, gerenciadores de estado, frameworks web). **Limite a no máximo 5 a 7 itens críticos**. Ignore pacotes de linting ou utilitários menores.
- **Domain:** Leia os nomes de rotas/endpoints, schemas e a lógica de negócios central para descrever, em **uma única linha concisa**, qual o propósito real do software.
- **Current Architecture:** Identifique a organização estrutural. A lógica está agrupada em scripts soltos/monolíticos ou já possui separação clara (Models, Controllers, Services, ViewCode, etc.)? Aponte a topologia atual.
- **Database:** Identifique o mecanismo de banco de dados utilizado. Liste as tabelas/entidades, lendo arquivos de migração ou definições de ORM, mas **limite-se apenas às 5-10 entidades principais do domínio** (ignore tabelas de migração interna, logs ou sessões).
- **Scope:** Conte os arquivos de código-fonte valiosos. **Exclua explicitamente**: dependências, arquivos de lock, `node_modules`, `.venv`, `.git`, pastas de build/dist e metadados.

**Formato de Saída Obrigatório (Imprima exatamente como abaixo, preenchendo os valores entre `< >` sem alterar o layout):**

================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      <...>
Framework:     <...>
Dependencies:  <...>
Domain:        <...>
Architecture:  <...>
Source files:  <N> files analyzed
DB tables:     <...>
================================