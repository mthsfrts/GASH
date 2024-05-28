# GitHub Actions Syntax

## Estrutura de Configurações do GitHub Actions
No GitHub Actions, a configuração de workflows é feita em três níveis: **workflow**, **job** e **step**. Abaixo está uma descrição detalhada das configurações possíveis em cada nível.

### Workflow

No nível do workflow, você define configurações gerais que se aplicam a todo o fluxo de trabalho:

```yaml
name: [workflow_name]

on:
  [push|pull_request|schedule|workflow_dispatch|workflow_call]: ...
  workflow_call:
    secrets:
      SECRET_NAME:
 required: true

env: # Variáveis de ambiente globais
  GLOBAL_VAR: value

defaults: # Configurações padrão para todos os jobs e steps
  run:
    shell: bash
    working-directory: scripts

inputs: # Entradas para o workflow (especialmente com workflow_dispatch e workflow_call)
  input_name:
    description: 'Description of the input'
    required: true
    default: 'default_value'
    type: string

outputs: # Saídas do workflow
  output_name: ${{ jobs.job_id.outputs.output_name }}

concurrency: # Limitar a execução simultânea de workflows
  group: workflow-group
  cancel-in-progress: true

permissions: # Permissões do GITHUB_TOKEN
  actions: read
  contents: read
```

### Job

O nível do job define um conjunto de steps que são executados em um ambiente específico:

```yaml
jobs:
  [job_id]:
    name: [job_name]
    runs-on: [runner]
    needs: [job_id]
    env: # Variáveis de ambiente específicas para o job
      JOB_VAR: value
    secrets: # Segredos específicos para o job
      SECRET_VAR: ${{ secrets.SECRET_NAME }}
    strategy:
      matrix: ...
      fail-fast: true
      max-parallel: 2
    concurrency: # Limitar a execução simultânea de jobs
      group: job-group
      cancel-in-progress: true
    steps: ...
    outputs: # Saídas do job, podem ser usadas por outros jobs
      output_id: ${{ steps.step_id.outputs.output_name }}
    timeout-minutes: [minutes]
    continue-on-error: [true|false]
    container: # Container Docker para executar o job
      image: [docker_image]
    services: # Serviços adicionais para o job (por exemplo, banco de dados)
      [service_name]: ...
    retries: # Configuração de reexecução do job
      max-attempts: [number]
    permissions: # Permissões do GITHUB_TOKEN para o job
      actions: read
      contents: read
    status-check: # Checks de status
      status: [success|failure|cancelled|skipped|timed_out|completed]
    artifacts: # Artefatos para upload/download
      upload:
       name: [artifact_name]
       path: [file_or_directory]
    download:
       name: [artifact_name]
       path: [destination_path]
```

### Step

O nível da step define ações ou comandos individuais a serem executados:

```yaml
steps:
  - name: [step_name]
    id: [step_id]
    if: [conditional]
    run: [command]
    uses: [action]
    with: ...
    env: # Variáveis de ambiente específicas para a step
      STEP_VAR: value
    continue-on-error: [true|false]
    timeout-minutes: [minutes]
    working-directory: [directory]
    retries: # Configuração de reexecução da step
      max-attempts: [number]
    status: [success|failure|cancelled|skipped|timed_out|completed]
    artifacts: # Artefatos para upload/download
      upload:
       name: [artifact_name]
       path: [file_or_directory]
    download:
       name: [artifact_name]
       path: [destination_path]
```

### Resumo das Configurações

Aqui está uma tabela resumida das configurações possíveis em cada nível, em ordem alfabética:

| Configuração      | Workflow | Job | Step |
|-------------------|----------|-----|------|
| artifacts         |          | ✔️  | ✔️   |
| concurrency       | ✔️       | ✔️  |      |
| container         |          | ✔️  |      |
| continue-on-error |          | ✔️  | ✔️   |
| defaults          | ✔️       |     |      |
| env               | ✔️       | ✔️  | ✔️   |
| fail-fast         |          | ✔️  |      |
| if                |          |     | ✔️   |
| inputs            | ✔️       |     |      |
| jobs              | ✔️       |     |      |
| max-parallel      |          | ✔️  |      |
| name              | ✔️       | ✔️  | ✔️   |
| needs             |          | ✔️  |      |
| on                | ✔️       |     |      |
| outputs           | ✔️       | ✔️  |      |
| permissions       | ✔️       | ✔️  |      |
| retries           |          | ✔️  | ✔️   |
| run               |          |     | ✔️   |
| runs-on           |          | ✔️  |      |
| secrets           | ✔️       | ✔️* |      |
| services          |          | ✔️  |      |
| steps             |          | ✔️  | ✔️   |
| strategy          |          | ✔️  |      |
| timeout-minutes   | ✔️       | ✔️  | ✔️   |
| uses              |          | ✔️  | ✔️   |
| with              |          | ✔️  | ✔️   |
| working-directory |          |     | ✔️   |

*Note: `secrets` no nível do job está em beta.

Essas configurações são baseadas nas informações das documentações oficiais do GitHub Actions:
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Contexts](https://docs.github.com/en/actions/learn-github-actions/contexts)
- [Variables](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Workflow commands](https://docs.github.com/en/actions/learn-github-actions/workflow-commands-for-github-actions)
- [Guides for GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/guides-for-github-actions)

# Smells para GitHub Actions
### Resumo dos Smells

### Categoria: Segurança

#### [ ] 1. **Hard-coded Secrets**
- **Estratégia:** Verificar a presença de segredos diretamente nos arquivos YAML.
- **Descrição:** Segredos e credenciais armazenados diretamente no código, expondo dados sensíveis.
- **Mitigação:** Utilizar GitHub Secrets para armazenar informações sensíveis.
- **Grau de Vulnerabilidade:** Crítico
  - **Justificativa:** Exposição de credenciais pode levar a comprometimentos graves de segurança.

#### [ ] 2. **Inefficient Use of Fail-Fast and Continue-on-Error**
- **Estratégia:** Verificar a configuração de `fail-fast` e `continue-on-error` para garantir que sejam usadas corretamente.
- **Descrição:** Configurações que podem levar a execuções desnecessárias ou mascarar falhas.
- **Mitigação:** Usar `fail-fast` e `continue-on-error` de forma adequada para garantir execuções eficientes e transparentes.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Pode mascarar problemas ou causar execuções desnecessárias, aumentando a complexidade de depuração.

#### [ ] 3. **Retry Failure**
- **Estratégia:** Identificar reexecuções automáticas que mascaram problemas reais.
- **Descrição:** Reexecuções automáticas que podem esconder problemas intermitentes.
- **Mitigação:** Investigar e corrigir as causas subjacentes das falhas em vez de reexecutar automaticamente.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Pode mascarar problemas que afetam a confiabilidade do sistema.

#### [ ] 4. **Deprecated or Unsafe Libraries**
- **Estratégia:** Verificar o uso de bibliotecas desatualizadas ou conhecidamente inseguras.
- **Descrição:** Uso de bibliotecas que não recebem mais atualizações ou que têm vulnerabilidades conhecidas.
- **Mitigação:** Manter as bibliotecas atualizadas e usar ferramentas de análise de dependências.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Pode introduzir vulnerabilidades conhecidas no sistema.

#### [ ] 5. **Flaky Tests**
- **Estratégia:** Detectar testes que falham de maneira intermitente.
- **Descrição:** Testes que falham aleatoriamente, causando incerteza nos resultados.
- **Mitigação:** Identificar e corrigir a causa raiz da flakiness dos testes.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Reduz a confiança nos resultados dos testes.

### Categoria: Manutenção

#### [ ] 1. **Push Event Misconfiguration**
- **Estratégia:** Verificar configurações de push associadas a branches e tags.
- **Descrição:** Má configuração dos eventos de push, como ausência de filtros para branches ou tags específicas.
- **Mitigação:** Usar filtros apropriados para branches e tags.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Pode levar à execução desnecessária de workflows e aumentar a carga do CI/CD.

#### [ ] 2. **Pull Request Event Misconfiguration**
- **Estratégia:** Verificar configurações de pull request associadas a branches específicas.
- **Descrição:** Má configuração dos eventos de pull request, como falta de filtros para branches específicas ou condições de merge.
- **Mitigação:** Usar filtros apropriados para branches e condições de merge.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Pode levar à execução desnecessária de workflows e a possíveis conflitos de merge.

#### [ ] 3. **Release Event Misconfiguration**
- **Estratégia:** Verificar configurações de release associadas a versões específicas.
- **Descrição:** Má configuração dos eventos de release, como ausência de filtros para versões específicas ou prereleases.
- **Mitigação:** Usar filtros apropriados para versões e prereleases.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Pode levar à execução desnecessária de workflows e a lançamento incorreto de versões.

#### [ ] 4. **Workflow Dispatch Misconfiguration**
- **Estratégia:** Verificar a configuração de inputs no evento de dispatch manual.
- **Descrição:** Má configuração dos inputs fornecidos manualmente no evento de dispatch.
- **Mitigação:** Validar e documentar claramente os inputs necessários para o dispatch manual.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Inputs incorretos podem levar à execução inadequada de workflows e falhas na execução.

#### [ ] 5. **Workflow Call Misconfiguration**
- **Estratégia:** Verificar a configuração de chamadas de outros workflows.
- **Descrição:** Má configuração de chamadas remotas de outros workflows, como falta de validação de parâmetros.
- **Mitigação:** Validar e documentar claramente os parâmetros passados nas chamadas de workflows.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Chamadas incorretas podem levar a falhas de execução e dependências não resolvidas.

#### [ ] 6. **Run Event Misconfiguration**
- **Estratégia:** Verificar a configuração do evento de run baseado no status de outros workflows.
- **Descrição:** Má configuração do evento de run, como dependências incorretas ou status de execução não configurados adequadamente.
- **Mitigação:** Configurar corretamente as dependências e status de execução.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Dependências incorretas podem levar a execuções desnecessárias ou falhas na execução.

#### [ ] 7. **Fuzzy Version**
- **Estratégia:** Detectar versões imprecisas ou ausentes em dependências.
- **Descrição:** Uso de versões não específicas para dependências, dificultando a reprodução de builds.
- **Mitigação:** Especificar versões exatas para todas as dependências.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Pode levar a inconsistências e dificuldades na manutenção.

#### [ ] 8. **Untracked Artifacts**
- **Estratégia:** Verificar se artefatos são gerados sem controle de versão.
- **Descrição:** Artefatos gerados que não são rastreados ou versionados, dificultando a reprodução.
- **Mitigação:** Implementar controle de versão para todos os artefatos.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Dificulta a reprodução e manutenção do ambiente de build.

#### [ ] 9. **Inefficient Cache Management**
- **Estratégia:** Verificar o uso correto e invalidação de caches.
- **Descrição:** Cache mal gerenciado que não é reutilizado ou cresce desnecessariamente.
- **Mitigação:** Configurar corretamente as chaves de cache e limpar caches regularmente.
- **Grau de Vulnerabilidade:** Pequeno
  - **Justificativa:** Impacta a eficiência, mas não compromete diretamente a segurança ou a funcionalidade.

#### [ ] 10. **Inadequate Logging**
- **Estratégia:** Verificar logs para presença de dados sensíveis ou excesso de informações.
- **Descrição:** Logs que expõem dados sensíveis ou são muito verbosos.
- **Mitigação:** Utilizar `::add-mask::` para mascarar dados sensíveis e adotar práticas de logging padrão.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Pode expor dados sensíveis e dificultar a depuração.

#### [ ] 11. **Complex Event Triggers**
- **Estratégia:** Verificar o uso de múltiplos triggers e a complexidade na configuração de eventos.
- **Descrição:** Configurações complexas de eventos que podem causar execuções indesejadas ou desnecessárias.
- **Mitigação:** Simplificar a configuração de eventos e documentar claramente a lógica de triggers.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Aumenta a complexidade e pode levar a execuções inesperadas.

#### [ ] 12. **Improper Use of Matrix Strategy**
- **Estratégia:** Verificar a configuração da matriz para variações desnecessárias ou excessivas.
- **Descrição:** Configurações de matriz que criam variações redundantes ou desnecessárias de jobs.
- **Mitigação:** Otimizar a configuração da matriz para evitar execuções redundantes.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Aumenta o tempo de execução e o uso de recursos.

#### [ ] 13. **Convoluted Conditions**
- **Estratégia:** Verificar o uso de condições complexas (`if`, `with`, `needs`, etc.) que podem ser simplificadas.
- **Descrição:** Uso de condições complexas que podem dificultar a leitura e manutenção do workflow.
- **Mitigação:** Simplificar condições e documentar claramente a lógica condicional.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Aumenta a complexidade e pode introduzir erros difíceis de depurar.

#### [ ] 14. **Misuse of Execution Status Checks**
- **Estratégia:** Verificar o uso correto de verificações de status de execução (`always`, `canceled`, `success`).
- **Descrição:** Uso inadequado de verificações de status que podem causar execuções indesejadas ou ignorar falhas.
- **Mitigação:** Configurar corretamente as verificações de status para garantir execuções adequadas.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Pode levar a execuções indesejadas ou mascarar falhas importantes.

#### [ ] 15. **Bash Script Complexity**
- **Estratégia:** Verificar scripts bash longos e complexos dentro dos steps.
- **Descrição:** Scripts bash complexos que podem ser difíceis de manter e depurar.
- **Mitigação:** Dividir scripts complexos em partes menores e mais gerenciáveis e adicionar comentários explicativos.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Dificulta a manutenção e aumenta a possibilidade de erros.

### Categoria: Eficiência

#### [ ] 1. **Long Build Times**
- **Estratégia:** Monitorar o tempo de execução dos builds e identificar etapas que causam lentidão.
- **Descrição:** Builds que demoram muito tempo, impactando a produtividade.
- **Mitigação:** Otimizar os passos do build e usar caching eficazmente.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Impacta a produtividade, mas não compromete diretamente a segurança ou a funcionalidade.

#### [ ] 2. **Excessive Privileges**
- **Estratégia:** Verificar permissões configuradas nos workflows.
- **Descrição:** Permissões excessivas configuradas nos workflows que podem levar a riscos de segurança.
- **Mitigação:** Restringir permissões aos mínimos necessários.
- **Vulnerabilidade:** 
  - **Grau:** Crítico
  - **Justificativa:** Permissões excessivas podem levar a comprometimentos graves de segurança.

### Categoria: Qualidade

#### [ ] 1. **Typos and Generic Words**
- **Estratégia:** Verificar nomes de jobs, steps e variáveis para identificar erros de digitação comuns ou termos muito genéricos.
- **Descrição:** Erros de digitação e palavras genéricas que dificultam a compreensão do código.
- **Mitigação:** Adotar convenções de nomenclatura claras e revisar o código regularmente.
- **Grau de Vulnerabilidade:** Pequeno
  - **Justificativa:** Impacta a legibilidade e manutenção, mas não compromete diretamente a segurança ou a funcionalidade.

#### [ ] 2. **Inconsistent Naming Conventions**
- **Estratégia:** Verificar se nomes de jobs, steps e variáveis seguem convenções consistentes.
- **Descrição:** Convenções de nomenclatura inconsistentes que dificultam a leitura e manutenção.
- **Mitigação:** Adotar e seguir convenções de nomenclatura claras.
- **Grau de Vulnerabilidade:** Pequeno
  - **Justificativa:** Impacta a legibilidade e manutenção, mas não compromete diretamente a segurança ou a funcionalidade.

#### [ ] 3. **Large Code Blocks**
- **Estratégia:** Identificar steps que contêm scripts longos e complexos.
- **Descrição:** Blocos de código grandes que dificultam a leitura e manutenção.
- **Mitigação:** Dividir scripts longos em partes menores e mais gerenciáveis.
- **Grau de Vulnerabilidade:** Médio
  - **Justificativa:** Impacta a legibilidade e manutenção, podendo levar a erros e dificuldades na depuração.

#### [ ] 4. **Lack of Comments and Documentation**
- **Estratégia:** Verificar a presença de comentários explicativos e documentação adequada.
- **Descrição:** Falta de comentários e documentação nos workflows.
- **Mitigação:** Adicionar comentários explicativos e manter a documentação atualizada.
- **Grau de Vulnerabilidade:** Pequeno
  - **Justificativa:** Impacta a legibilidade e manutenção, mas não compromete diretamente a segurança ou a funcionalidade.