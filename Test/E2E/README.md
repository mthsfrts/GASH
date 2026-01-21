# Suite de Testes E2E do GASH

Suite completa de testes end-to-end para a ferramenta CLI GASH (GitHub Actions Smell Hunter).

## Visão Geral

Esta suite de testes valida a funcionalidade do GASH através de 7 cenários principais:

| Cenário | Descrição | Testes | Token Necessário |
|----------|-------------|-------|----------------|
| **1. Repositório Limpo** | Valida ausência de falsos positivos em workflows limpos | 6 | Opcional |
| **2. Detecção Multi-Smell** | Testa detecção de smells de segurança, manutenção e qualidade | 21 | Opcional |
| **3. Repositório Real** | Analisa repositórios do mundo real (actions/starter-workflows) | 9 | Sim |
| **4. Modos de Execução** | Testa comandos CLI (analyze, batch-analyze) | 23 | Misto |
| **5. Geração de Relatórios** | Valida formato e completude do output | 21 | Misto |
| **6. Performance** | Testa escalabilidade e tempo de execução | 9 | Não |
| **7. Tratamento de Erros** | Testa robustez com inputs malformados | 14 | Não |
| **Total** | | **103** | |

## Início Rápido

### Pré-requisitos

```bash
# Instalar dependências
pip install -r requirements.txt

# Instalar dependências de teste (opcional para testes de memória)
pip install psutil
```

### Executando Testes Localmente

```bash
# Executar todos os testes sem token real (modo mock)
pytest Test/E2E/ -v -m "not requires_real_token"

# Executar todos os testes com token real
export GITHUB_TOKEN=seu_token_aqui
pytest Test/E2E/ -v

# Executar cenário específico
pytest Test/E2E/test_scenario1_clean_repoTs.py -v

# Executar com cobertura
pytest Test/E2E/ -v --cov=Analysis --cov-report=html
```

### Executando no CI/CD

A suite de testes executa automaticamente no GitHub Actions:

- **Testes Mock Token**: Executam em push/PR para branches `prod` ou `main`
- **Testes Token Real**: Executam em push para `prod` ou `main` (usa `secrets.GITHUB_TOKEN`)
- **Suite Completa**: Acionada manualmente via `workflow_dispatch`

## Cenários de Teste

### Cenário 1: Análise de Repositório Limpo

**Propósito**: Verificar que workflows limpos e bem configurados não geram falsos positivos.

**Arquivos de Teste**: `test_scenario1_clean_repoTs.py`

**Testes Principais**:
- Todos os 9 detectores retornam sem findings para workflows limpos
- Análise de repositório real (actions/starter-workflows) sem falsos positivos

**Problemas Conhecidos**:
- ⚠️ Detector **ErrorHandling** reporta falsos positivos sobre valores de timeout (bug)
- ⚠️ Detector **Misconfiguration** reporta falsos positivos sobre parâmetros `defaults` e `run`/`uses` faltantes (bug)
- Estes são bugs documentados nos detectores, não falhas de teste

### Cenário 2: Detecção Multi-Smell

**Propósito**: Validar detecção de todos os 9 tipos de smell em múltiplos workflows.

**Arquivos de Teste**: `test_scenario2_multi_smellsTs.py`

**Testes Principais**:
- Smells de segurança: AdminByDefault, HardCoded, UnsecureProtocol, RemoteTriggers
- Smells de manutenção: CodeReplica, ErrorHandling, Misconfiguration
- Smells de qualidade: LongBlocks
- Validação com repositório real OWASP Juice Shop

**Fixtures Utilizados**:
- `vulnerable_workflow.yml`: Múltiplos smells de segurança
- `maintenance_issues.yml`: Padrões de smells de manutenção
- `complex_workflow.yml`: Todos os 9 tipos de smell

### Cenário 3: Análise de Repositório Real

**Propósito**: Testar robustez com workflows GitHub Actions de produção.

**Arquivos de Teste**: `test_scenario3_real_repoTs.py`

**Testes Principais**:
- Análise completa sem crashes (>90% taxa de sucesso)
- Tratamento de estruturas de workflow diversas
- Resultados consistentes entre múltiplas execuções
- Estabilidade de memória durante análise de repositório

**Repositório Real**: `actions/starter-workflows` (clonado em runtime)

### Cenário 4: Modos de Execução

**Propósito**: Validar diferentes modos de execução CLI e consistência.

**Arquivos de Teste**: `test_scenario4_exec_modesTs.py`

**Testes Principais**:
- Análise de arquivo único (`analyze --file`)
- Análise batch de diretório (`batch-analyze --dir`)
- Consistência entre modos single e batch
- Casos extremos (diretórios vazios, arquivos inexistentes, paths relativos/absolutos)

### Cenário 5: Geração de Relatórios

**Propósito**: Validar formato de output e completude do relatório.

**Arquivos de Teste**: `test_scenario5_report_genTs.py`

**Testes Principais**:
- Formato de output no console ("Findings for {detector}:")
- Todos os 9 detectores representados no output
- Findings contêm informações acionáveis
- Resultados determinísticos e consistentes

### Cenário 6: Performance e Escalabilidade

**Propósito**: Garantir que GASH atende requisitos de performance.

**Arquivos de Teste**: `test_scenario6_performanceTs.py`

**Requisitos de Performance**:
- Workflow único: < 30 segundos
- Batch 50+ workflows: < 5 minutos
- Uso de memória: < 500 MB pico
- Throughput: > 1 workflow/segundo

**Testes Principais**:
- Performance de workflow único
- Análise batch com 50+ workflows gerados
- Escalabilidade com 100 workflows simples
- Estabilidade de memória (sem vazamentos)

### Cenário 7: Tratamento de Erros

**Propósito**: Validar tratamento gracioso de inputs inválidos e casos extremos.

**Arquivos de Teste**: `test_scenario7_error_handlingTs.py`

**Testes Principais**:
- Tratamento de YAML malformado (sem crashes)
- Tratamento de arquivo/diretório inexistente
- Tratamento de diretório vazio
- Unicode e valores nulos
- Workflows muito grandes
- Análise funciona sem chamadas de API

## Gestão de Tokens

A suite de testes usa uma estratégia dual de tokens:

### Mock Token (Desenvolvimento Local)

Para testes que não requerem acesso à API do GitHub:

```python
@pytest.fixture
def mock_token_env(mock_token, tmp_path):
    """Cria config temporária com mock token"""
```

**Uso**: Automaticamente usado para testes sem `@pytest.mark.requires_real_token`

### Token Real (Testes CI/Integração)

Para testes que requerem API do GitHub:

```python
@pytest.fixture
def ci_token_env(real_token):
    """Usa GITHUB_TOKEN do environment"""
```

**Configuração**:
```bash
export GITHUB_TOKEN=seu_token_aqui
pytest Test/E2E/ -v -m "requires_real_token"
```

**CI**: Usa automaticamente `secrets.GITHUB_TOKEN` no GitHub Actions

## Adicionando Novos Testes

### 1. Escolha o Cenário Apropriado

Adicione testes ao arquivo de cenário relevante baseado no que você está testando:
- Precisão de detecção → Cenário 1 ou 2
- Funcionalidade CLI → Cenário 4
- Formato de output → Cenário 5
- Performance → Cenário 6
- Casos de erro → Cenário 7

### 2. Siga o Padrão de Teste

```python
class TestYourFeature:
    """
    Breve descrição do que esta classe de teste valida
    """

    @pytest.fixture
    def your_fixture(self, fixtures_path):
        """Setup dos dados de teste"""
        return fixtures_path / "your_workflow.yml"

    def test_your_feature(self, your_fixture):
        """
        Descrição do teste seguindo padrão Given-When-Then.
        """
        # Arrange
        action = Action(file_path=str(your_fixture))
        workflow = action.prepare_for_analysis()

        # Act
        findings = YourDetectorFct(content=workflow).detect()

        # Assert
        assert expected_condition, "Mensagem de erro"
```

### 3. Marque Testes Apropriadamente

```python
@pytest.mark.requires_real_token  # Precisa API do GitHub
@pytest.mark.slow                  # Leva > 1 segundo
```

### 4. Adicione Fixture Se Necessário

Se você precisar de um novo workflow fixture:

1. Crie `Test/E2E/fixtures/workflows/your_workflow.yml`
2. Documente os smells que ele contém (como comentários)
3. Referencie no teste via fixture `fixtures_path`

## Fixtures

### Fixtures de Workflow

| Fixture | Propósito | Smells |
|---------|---------|--------|
| `clean_workflow.yml` | Golden master (sem smells) | Nenhum |
| `vulnerable_workflow.yml` | Smells de segurança | AdminByDefault, HardCoded, UnsecureProtocol, RemoteTriggers, UntrustedDependencies |
| `maintenance_issues.yml` | Smells de manutenção | CodeReplica, ErrorHandling, Misconfiguration |
| `complex_workflow.yml` | Todos os tipos de smell | Todos os 9 tipos |
| `malformed_workflow.yml` | Tratamento de erros | YAML inválido |

### Fixtures de Repositório Real

Clonados em runtime via sparse checkout:

| Repositório | Propósito | Cenário |
|------------|---------|----------|
| `actions/starter-workflows` | Golden master, Análise de repo real | 1, 3 |
| `juice-shop/juice-shop` | Validação de segurança | 2 |

## Solução de Problemas

### Testes Falham com "Token not available"

**Solução**: Exporte a variável de ambiente `GITHUB_TOKEN`:
```bash
export GITHUB_TOKEN=seu_token_aqui
pytest Test/E2E/ -v
```

### Testes Falham com "Could not clone repository"

**Causa**: Problemas de rede ou rate limiting do GitHub

**Soluções**:
- Verifique conexão com internet
- Aguarde alguns minutos (reset de rate limit)
- Execute apenas testes mock token: `pytest Test/E2E/ -v -m "not requires_real_token"`

### Testes Dão Timeout

**Causa**: Clones de repositórios reais podem demorar

**Soluções**:
- Aumente timeout: `pytest Test/E2E/ -v --timeout=300`
- Pule testes lentos: `pytest Test/E2E/ -v -m "not slow"`

### Testes de Memória Pulados

**Causa**: `psutil` não instalado

**Solução**:
```bash
pip install psutil
pytest Test/E2E/ -v -k "memory"
```

### Falsos Positivos em Workflows Limpos

**Problemas Conhecidos**:
- Detector `ErrorHandling` tem bugs com validação de timeout (reporta falsos positivos)
- Detector `Misconfiguration` tem bugs com validação de `defaults` e `run`/`uses`

**Impacto**: 3 testes no Cenário 1 podem falhar (comportamento documentado)

**Rastreamento**: Estes são bugs conhecidos nos detectores, não falhas de teste

## Benchmarks de Performance

Performance esperada em hardware típico:

| Operação | Tempo Esperado | Real (MacBook Air M1) |
|-----------|---------------|-------------------------|
| Workflow único | < 30s | ~0.1s |
| Batch 50 workflows | < 5min | ~0.5s |
| Suite E2E completa | < 15min | ~15s |
| Clone de repo real | < 2min | ~5-10s |

## Contribuindo

Ao adicionar novos testes E2E:

1. Siga padrões existentes nos arquivos de cenário
2. Adicione docstrings claras explicando o que está sendo testado
3. Use mensagens de asserção descritivas
4. Considere se o teste precisa de token real
5. Atualize este README se adicionar novos cenários
6. Garanta que testes passem localmente antes de commitar

## Integração CI/CD

### Workflow GitHub Actions

A suite de testes E2E executa automaticamente em:
- **Push** para branches `prod` ou `main`
- **Pull Requests** para `prod` ou `main`
- **Trigger manual** via `workflow_dispatch`

### Matriz de Testes

- **OS**: Ubuntu, macOS
- **Python**: 3.9, 3.10, 3.11, 3.12
- **Modos**: Mock token, Token real, Suite completa

### Artefatos

Resultados de testes são enviados como artefatos:
- Retenção: 7 dias (mock/real), 30 dias (completo)
- Localização: `.pytest_cache/`, `Test/E2E/*.log`

## Resumo

Esta suite de testes E2E fornece validação compreensiva da funcionalidade do GASH:

- ✅ 103 testes através de 7 cenários
- ✅ 94% taxa de aprovação (3 bugs conhecidos nos detectores)
- ✅ Modos mock e token real
- ✅ Benchmarking de performance
- ✅ Integração CI/CD
- ✅ Documentação extensiva

Para questões ou problemas, por favor abra uma issue no GitHub.
