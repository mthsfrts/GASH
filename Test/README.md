# Testes de Segurança *Error Handling*

Esta parte do projeto contém **fixtures e testes automatizados** destinados a identificar **más práticas de segurança e manutenção** em *pushes* de códigos no GASH. Cada fixture representa um cenário específico que deve ser detectado pelo *checker*.

---

## Estrutura dos Testes

Cada teste segue o mesmo padrão:
1. Carrega um arquivo `.yml` representando um workflow
2. Executa uma verificação específica ou genérica
3. Avalia se o comportamento esperado foi identificado

---

## Fixtures Documentadas

### 1) `steps_no_error_handling.yml`
**Teste:** `Test/Fixtures/ErrorHandling/steps_no_error_handling.yml`

**O que testa:**  
Detecta **fluxos de trabalho** que executam comandos CRÍTICOS **sem qualquer tratamento explícito de erro prévio**.

**Problema identificado:**  
*Lack of Error Handling* — comandos podem falhar silenciosamente ou causar comportamento inesperado no pipeline.

**Risco:**  
- Builds quebradas  
- Estados inconsistentes  
- Comprometimento da integridade do processo  

---

### 2) `inadequate_continue_on_error.yml`
**Teste:** `Test/Fixtures/ErrorHandling/inadequate_continue_on_error.yml`

**O que testa:**  
Identifica o uso **inadequado** de `continue-on-error: true` em jobs ou etapas críticas. Em geral, permanecer com o código funcionando, mesmo a custo de um erro crítico aceito, pode custar muito para a segurança de qualquer projeto - seja privado, seja de fonte aberta.

**Problema identificado:**  
*Inadequate Continue on Error* — falhas graves são ignoradas e o pipeline continua como se tivesse sucesso.

**Risco:**  
- Deploys incompletos  
- Falsa sensação de sucesso  
- Sistemas em estado inconsistente  

---

### 3) `missing_output_validation.yml`
**Teste:** `Test/Fixtures/ErrorHandling/missing_output_validation.yml`

**O que testa:**  
Verifica fluxos de trabalho que utilizam **outputs de comandos/passos dados anteriormente, e que são repassados para outros processos sem validação prévia**.

**Problema identificado:**  
*Missing Output Validation* — valores derivados de outros steps são reutilizados sem checagem de conteúdo ou formato.

**Risco:**  
- Falhas lógicas  
- Execução de fluxos incorretos  
- Possível comportamento inesperado  

---

### 4) `no_retry_logic.yml`
**Teste:** `Test/Fixtures/ErrorHandling/no_retry_logic.yml`

**O que testa:**  
Detecta operações suscetíveis a falhas temporárias (ex.: rede, APIs) **sem lógica de retry**. Isto significa que um processo pode ser interrompido por um erro imprevisível e momentâneo (instabilidade na rede, por exemplo) e mesmo assim não tornará a uma nova tentativa para ser testado.

**Problema identificado:**  
*No Retry Logic* — o pipeline falha na primeira tentativa, mesmo em erros transitórios.

**Risco:**  
- Instabilidade do CI/CD  
- Falhas intermitentes difíceis de diagnosticar  
- Baixa resiliência do processo  

---

## Objetivo dos Testes

Esses testes garantem que o *checker*:

- Reconheça padrões inseguros em workflows
- Retorne resultados consistentes
- Ajude a prevenir falhas de segurança e manutenção em CI/CD

---

## Observação Final

Nem todos os testes exigem a detecção obrigatória de vulnerabilidades; alguns validam apenas que o *checker* **analisa corretamente o cenário** e retorna resultados estruturados.
