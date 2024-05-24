# Smells para GitHub Actions

### Categoria: Segurança

#### [ ] 1. **Hard-coded Secrets**

- **Estratégia:** Verificar a presença de segredos diretamente nos arquivos YAML.
- **Impacto:** Crítico
- **Descrição:** Segredos e credenciais armazenados diretamente no código, expondo dados sensíveis.
- **Mitigação:** Utilizar GitHub Secrets para armazenar informações sensíveis.
- **Grau de Vulnerabilidade:** Crítico
    - **Justificativa:** Exposição de credenciais pode levar a comprometimentos graves de segurança.

#### [ ] 2. **Inefficient Use of Fail-Fast and Continue-on-Error**

- **Estratégia:** Verificar a configuração de `fail-fast` e `continue-on-error` para garantir que sejam usadas
  corretamente.
- **Impacto:** Médio
- **Descrição:** Configurações que podem levar a execuções desnecessárias ou mascarar falhas.
- **Mitigação:** Usar `fail-fast` e `continue-on-error` de forma adequada para garantir execuções eficientes e
  transparentes.
- **Grau de Vulnerabilidade:** Médio
    - **Justificativa:** Pode mascarar problemas ou causar execuções desnecessárias, aumentando a complexidade de
      depuração.

#### [ ] 3. **Retry Failure**

- **Estratégia:** Identificar reexecuções automáticas que mascaram problemas reais.
- **Impacto:** Médio
- **Descrição:** Reexecuções automáticas que podem esconder problemas intermitentes.
- **Mitigação:** Investigar e corrigir as causas subjacentes das falhas em vez de reexecutar automaticamente.
- **Grau de Vulnerabilidade:** Médio
    - **Justificativa:** Pode mascarar problemas que afetam a confiabilidade do sistema.

#### [ ] 4. **Deprecated or Unsafe Libraries**

- **Estratégia:** Verificar o uso de bibliotecas desatualizadas ou conhecidamente inseguras.
- **Impacto:** Médio
- **Descrição:** Uso de bibliotecas que não recebem mais atualizações ou que têm vulnerabilidades conhecidas.
- **Mitigação:** Manter as bibliotecas atualizadas e usar ferramentas de análise de dependências.
- **Grau de Vulnerabilidade:** Médio
    - **Justificativa:** Pode introduzir vulnerabilidades conhecidas no sistema.

#### [ ] 5. **Flaky Tests**

- **Estratégia:** Detectar testes que falham de maneira intermitente.
- **Impacto:** Médio
- **Descrição:** Testes que falham aleatoriamente, causando incerteza nos resultados.
- **Mitigação:** Identificar e corrigir a causa raiz da flakiness dos testes.
- **Grau de Vulnerabilidade:** Médio
    - **Justificativa:** Reduz a confiança nos resultados dos testes.

### Categoria: Manutenção

#### [ ] 1. **Fuzzy Version**

- **Estratégia:** Detectar versões imprecisas ou ausentes em dependências.
- **Impacto:** Médio
- **Descrição:** Uso de versões não específicas para dependências, dificultando a reprodução de builds.
- **Mitigação:** Especificar versões exatas para todas as dependências.
- **Grau de Vulnerabilidade:** Médio
    - **Justificativa:** Pode levar a inconsistências e dificuldades na manutenção.

#### [ ] 2. **Untracked Artifacts**

- **Estratégia:** Verificar se artefatos são gerados sem controle de versão.
- **Impacto:** Médio
- **Descrição:** Artefatos gerados que não são rastreados ou versionados, dificultando a reprodução.
- **Mitigação:** Implementar controle de versão para todos os artefatos.
- **Grau de Vulnerabilidade:** Médio
    - **Justificativa:** Dificulta a reprodução e manutenção do ambiente de build.

#### [ ] 3. **Inefficient Cache Management**

- **Estratégia:** Verificar o uso correto e invalidação de caches.
- **Impacto:** Pequeno
- **Descrição:** Cache mal gerenciado que não é reutilizado ou cresce desnecessariamente.
- **Mitigação:** Configurar corretamente as chaves de cache e limpar caches regularmente.
- **Grau de Vulnerabilidade:** Pequeno
    - **Justificativa:** Impacta a eficiência, mas não compromete diretamente a segurança ou a funcionalidade.

#### [ ] 4. **Inadequate Logging**

- **Estratégia:** Verificar logs para presença de dados sensíveis ou excesso de informações.
- **Impacto:** Médio
- **Descrição:** Logs que expõem dados sensíveis ou são muito verbosos.
- **Mitigação:** Utilizar `::add-mask::` para mascarar dados sensíveis e adotar práticas de logging padrão.
- **Grau de Vulnerabilidade:** Médio
    - **Justificativa:** Pode expor dados sensíveis e dificultar a depuração.

#### [ ] 5. **Complex Event Triggers (Triggers de Eventos Complexos)**

- **Estratégia:** Verificar o uso de múltiplos triggers e a complexidade na configuração de eventos.
- **Impacto:** Médio
- **Descrição:** Configurações complexas de eventos que podem causar execuções indesejadas ou desnecessárias.
- **Mitigação:** Simplificar a configuração de eventos e documentar claramente a lógica de triggers.
- **Grau de Vulnerabilidade:** Médio
    - **Justificativa:** Aumenta a complexidade e pode levar a execuções inesperadas.

#### [ ] 6. **Improper Use of Matrix Strategy**

- **Estratégia:** Verificar a configuração da matriz para variações desnecessárias ou excessivas.
- **Impacto:** Médio
- **Descrição:** Configurações de matriz que criam variações redundantes ou desnecessárias de jobs.
- **Mitigação:** Otimizar a configuração da matriz para evitar execuções redundantes.
- **Grau de Vulnerabilidade:** Médio
    - **Justificativa:** Aumenta o tempo de execução e o uso de recursos.

#### [ ] 7. **Convoluted Conditions (Condições Convolutas)**

- **Estratégia:** Verificar o uso de condições complexas (`if`, `with`, `needs`, etc.) que podem ser simplificadas.
- **Impacto:** Médio
- **Descrição:** Uso de condições complexas que podem dificultar a leitura e manutenção do workflow.
- **Mitigação:** Simplificar condições e documentar claramente a lógica condicional.
- **Grau de Vulnerabilidade:** Médio
    - **Justificativa:** Aumenta a complexidade e pode introduzir erros difíceis de depurar.

#### [ ] 8. **Misuse of Execution Status Checks (always, canceled, success)**

- **Estratégia:** Verificar o uso correto de verificações de status de execução (`always`, `canceled`, `success`).
- **Impacto:** Médio
- **Descrição:** Uso inadequado de verificações de status que podem causar execuções indesejadas ou ignorar falhas.
- **Mitigação:** Configurar corretamente as verificações de status para garantir execuções adequadas.
- **Grau de Vulnerabilidade:** Médio
    - **Justificativa:** Pode levar a execuções indesejadas ou mascarar falhas importantes.

#### [ ] 9. **Bash Script Complexity**

- **Estratégia:** Verificar scripts bash longos e complexos dentro dos steps.
- **Impacto:** Médio
- **Descrição:** Scripts bash complexos que podem ser difíceis de manter e depurar.
- **Mitigação:** Dividir scripts complexos em partes menores e mais gerenciáveis e adicionar comentários explicativos.
- **Grau de Vulnerabilidade:** Médio
    - **Justificativa:** Dificulta a manutenção e aumenta a possibilidade de erros.

### Categoria: Eficiência

#### [ ] 1. **Long Build Times**

- **Estratégia:** Monitorar o tempo de execução dos builds e identificar etapas que causam lentidão.
- **Impacto:** Médio
- **Descrição:** Builds que demoram muito tempo, impactando a produtividade.
- **Mitigação:** Otimizar os passos do build e usar caching eficazmente.
- **Grau de Vulnerabilidade:** Médio
    - **Justificativa:** Impacta a produtividade, mas não compromete diretamente a segurança ou a funcionalidade.

#### [ ] 2. **Excessive Privileges**

- **Estratégia:** Verificar permissões configuradas nos workflows.
- **Impacto:** Crítico
- **Descrição:** Permissões excessivas configuradas nos workflows que podem levar a riscos de segurança.
- **Mitigação:** Restringir permissões aos mínimos necessários.
- **Grau de Vulnerabilidade:** Crítico
    - **Justificativa:** Permissões excessivas podem levar a comprometimentos graves de segurança.

### Categoria: Qualidade

#### [ ] 1. **Typos and Generic Words**

- **Estratégia:** Verificar nomes de jobs, steps e variáveis para identificar erros de digitação comuns ou termos muito
  genéricos.
- **Impacto:** Pequeno
- **Descrição:** Erros de digitação e palavras genéricas que dificultam a compreensão do código.
- **Mitigação:** Adotar convenções de nomenclatura claras e revisar o código regularmente.
- **Grau de Vulnerabilidade:** Pequeno
    - **Justificativa:** Impacta a legibilidade e manutenção, mas não compromete diretamente a segurança ou a
      funcionalidade.

#### [ ] 2. **Inconsistent Naming Conventions**

- **Estratégia:** Verificar se nomes de jobs, steps e variáveis seguem convenções consistentes.
- **Impacto:** Pequeno
- **Descrição:** Convenções de nomenclatura inconsistentes que dificultam a leitura e manutenção.
- **Mitigação:** Adotar e seguir convenções de nomenclatura claras.
- **Grau de Vulnerabilidade:** Pequeno
    - **Justificativa:** Impacta a legibilidade e manutenção, mas não compromete diretamente a segurança ou a
      funcionalidade.

#### [ ] 3. **Large Code Blocks**

- **Estratégia:** Identificar steps que contêm scripts longos e complexos.
- **Impacto:** Médio
- **Descrição:** Blocos de código grandes que dificultam a leitura e manutenção.
- **Mitigação:** Dividir scripts longos em partes menores e mais gerenciáveis.
- **Grau de Vulnerabilidade:** Médio
    - **Justificativa:** Impacta a legibilidade e manutenção, podendo levar a erros e dificuldades na depuração.

#### [ ] 4. **Lack of Comments and Documentation**

- **Estratégia:** Verificar a presença de comentários explicativos e documentação adequada.
- **Impacto:** Pequeno
- **Descrição:** Falta de comentários e documentação nos workflows.
- **Mitigação:** Adicionar comentários explicativos e manter a documentação atualizada.
- **Grau de Vulnerabilidade:** Pequeno
    - **Justificativa:** Impacta a legibilidade e manutenção, mas não compromete diretamente a segurança ou a
      funcionalidade.

# Smells for GitHub Actions

### Category: Security

#### [ ] 1. **Hard-coded Secrets**

- **Strategy:** Check for secrets directly in YAML files.
- **Impact:** Critical
- **Description:** Secrets and credentials stored directly in the code, exposing sensitive information.
- **Mitigation:** Use GitHub Secrets to store sensitive information.
- **Vulnerability Level:** Critical
    - **Justification:** Exposure of credentials can lead to severe security breaches.

#### [ ] 2. **Inefficient Use of Fail-Fast and Continue-on-Error**

- **Strategy:** Verify the configuration of `fail-fast` and `continue-on-error` to ensure they are used correctly.
- **Impact:** Medium
- **Description:** Configurations that can lead to unnecessary executions or mask failures.
- **Mitigation:** Use `fail-fast` and `continue-on-error` appropriately to ensure efficient and transparent executions.
- **Vulnerability Level:** Medium
    - **Justification:** Can mask issues or cause unnecessary executions, increasing debugging complexity.

#### [ ] 3. **Retry Failure**

- **Strategy:** Identify automatic retries that mask real issues.
- **Impact:** Medium
- **Description:** Automatic retries that can hide intermittent issues.
- **Mitigation:** Investigate and fix the underlying causes of failures instead of automatically retrying.
- **Vulnerability Level:** Medium
    - **Justification:** Can mask issues that affect the system's reliability.

#### [ ] 4. **Deprecated or Unsafe Libraries**

- **Strategy:** Check for the use of outdated or known unsafe libraries.
- **Impact:** Medium
- **Description:** Use of libraries that no longer receive updates or have known vulnerabilities.
- **Mitigation:** Keep libraries updated and use dependency analysis tools.
- **Vulnerability Level:** Medium
    - **Justification:** Can introduce known vulnerabilities into the system.

#### [ ] 5. **Flaky Tests**

- **Strategy:** Detect tests that fail intermittently.
- **Impact:** Medium
- **Description:** Tests that fail randomly, causing uncertainty in results.
- **Mitigation:** Identify and fix the root cause of flaky tests.
- **Vulnerability Level:** Medium
    - **Justification:** Reduces confidence in test results.

### Category: Maintenance

#### [ ] 1. **Fuzzy Version**

- **Strategy:** Detect imprecise or missing versions in dependencies.
- **Impact:** Medium
- **Description:** Use of non-specific versions for dependencies, making build reproduction difficult.
- **Mitigation:** Specify exact versions for all dependencies.
- **Vulnerability Level:** Medium
    - **Justification:** Can lead to inconsistencies and maintenance difficulties.

#### [ ] 2. **Untracked Artifacts**

- **Strategy:** Check if artifacts are generated without version control.
- **Impact:** Medium
- **Description:** Generated artifacts that are not tracked or versioned, making reproduction difficult.
- **Mitigation:** Implement version control for all artifacts.
- **Vulnerability Level:** Medium
    - **Justification:** Makes reproducing and maintaining the build environment difficult.

#### [ ] 3. **Inefficient Cache Management**

- **Strategy:** Verify correct usage and invalidation of caches.
- **Impact:** Low
- **Description:** Poorly managed cache that is not reused or grows unnecessarily.
- **Mitigation:** Configure cache keys correctly and clean caches regularly.
- **Vulnerability Level:** Low
    - **Justification:** Impacts efficiency but does not directly compromise security or functionality.

#### [ ] 4. **Inadequate Logging**

- **Strategy:** Check logs for sensitive data or excessive information.
- **Impact:** Medium
- **Description:** Logs that expose sensitive data or are too verbose.
- **Mitigation:** Use `::add-mask::` to mask sensitive data and adopt standard logging practices.
- **Vulnerability Level:** Medium
    - **Justification:** Can expose sensitive data and hinder debugging.

#### [ ] 5. **Complex Event Triggers**

- **Strategy:** Verify the use of multiple triggers and the complexity in event configuration.
- **Impact:** Medium
- **Description:** Complex event configurations that can cause unwanted or unnecessary executions.
- **Mitigation:** Simplify event configuration and clearly document trigger logic.
- **Vulnerability Level:** Medium
    - **Justification:** Increases complexity and can lead to unexpected executions.

#### [ ] 6. **Improper Use of Matrix Strategy**

- **Strategy:** Verify matrix configuration for unnecessary or excessive variations.
- **Impact:** Medium
- **Description:** Matrix configurations that create redundant or unnecessary job variations.
- **Mitigation:** Optimize matrix configuration to avoid redundant executions.
- **Vulnerability Level:** Medium
    - **Justification:** Increases execution time and resource usage.

#### [ ] 7. **Convoluted Conditions**

- **Strategy:** Check for complex conditions (`if`, `with`, `needs`, etc.) that can be simplified.
- **Impact:** Medium
- **Description:** Use of complex conditions that can make the workflow hard to read and maintain.
- **Mitigation:** Simplify conditions and clearly document conditional logic.
- **Vulnerability Level:** Medium
    - **Justification:** Increases complexity and can introduce hard-to-debug errors.

#### [ ] 8. **Misuse of Execution Status Checks**

- **Strategy:** Verify correct usage of execution status checks (`always`, `canceled`, `success`).
- **Impact:** Medium
- **Description:** Incorrect use of status checks that can cause unwanted executions or ignore failures.
- **Mitigation:** Configure status checks correctly to ensure proper executions.
- **Vulnerability Level:** Medium
    - **Justification:** Can lead to unwanted executions or mask important failures.

#### [ ] 9. **Bash Script Complexity**

- **Strategy:** Check for long and complex bash scripts within steps.
- **Impact:** Medium
- **Description:** Complex bash scripts that can be hard to maintain and debug.
- **Mitigation:** Split complex scripts into smaller, more manageable parts and add explanatory comments.
- **Vulnerability Level:** Medium
    - **Justification:** Makes maintenance difficult and increases the likelihood of errors.

### Category: Efficiency

#### [ ] 1. **Long Build Times**

- **Strategy:** Monitor build times and identify steps causing delays.
- **Impact:** Medium
- **Description:** Builds that take a long time, impacting productivity.
- **Mitigation:** Optimize build steps and use effective caching.
- **Vulnerability Level:** Medium
    - **Justification:** Impacts productivity but does not directly compromise security or functionality.

#### [ ] 2. **Excessive Privileges**

- **Strategy:** Check permissions configured in workflows.
- **Impact:** Critical
- **Description:** Excessive permissions configured in workflows that can lead to security risks.
- **Mitigation:** Restrict permissions to the minimum necessary.
- **Vulnerability Level:** Critical
    - **Justification:** Excessive permissions can lead to severe security breaches.

### Category: Quality

#### [ ] 1. **Typos and Generic Words**

- **Strategy:** Check job, step, and variable names for common typos or overly generic terms.
- **Impact:** Low
- **Description:** Typos and generic words that make the code harder to understand.
- **Mitigation:** Adopt clear naming conventions and regularly review the code.
- **Vulnerability Level:** Low
    - **Justification:** Impacts readability and maintenance but does not directly compromise security or functionality.

#### [ ] 2. **Inconsistent Naming Conventions**

- **Strategy:** Verify that job, step, and variable names follow consistent conventions.
- **Impact:** Low
- **Description:** Inconsistent naming conventions that make the code harder to read and maintain.
- **Mitigation:** Adopt and follow clear naming conventions.
- **Vulnerability Level:** Low
    - **Justification:** Impacts readability and maintenance but does not directly compromise security or functionality.

#### [ ] 3. **Large Code Blocks**

- **Strategy:** Identify steps containing long and complex scripts.
- **Impact:** Medium
- **Description:** Large code blocks that make the code harder to read and maintain.
- **Mitigation:** Split long scripts into smaller, more manageable parts.
- **Vulnerability Level:** Medium
    - **Justification:** Impacts readability and maintenance, potentially leading to errors and debugging difficulties.

#### [ ] 4. **Lack of Comments and Documentation**

- **Strategy:** Check for the presence of explanatory comments and adequate documentation.
- **Impact:** Low
- **Description:** Lack of comments and documentation in workflows.
- **Mitigation:** Add explanatory comments and keep documentation up to date.
- **Vulnerability Level:** Low
    - **Justification:** Impacts readability and maintenance but does not directly compromise security or functionality.