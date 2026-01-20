# Contribuindo para o GASH

Obrigado pelo interesse em contribuir com o **GASH (GitHub Actions Smell Hunter)**! Somos um projeto Open Source e dependemos da colaboração da comunidade para evoluir nossa ferramenta de detecção de *smells* em CI/CD. O objetivo deste documento é definir um conjunto de boas práticas e processos para lhe auxiliar na manutenibilidade do projeto.

Este guia detalha como configurar o ambiente, entender a estrutura do código e submeter suas contribuições.

---

## Primeiros Passos

### Pré-requisitos
Como o GASH é construído em Python, você precisará ter instalado:
- **Python 3.8+**
- **Git**

### Configurando o Ambiente de Desenvolvimento
Para rodar o GASH localmente e testar suas alterações:

1.  **Faça o Fork e Clone o repositório:**
    ```bash
    git clone git@github.com:mthsfrts/GASH.git
    cd GASH
    ```

2.  **Instale as dependências:**
    Utilizamos o arquivo `requirements.txt` para gerenciar os pacotes.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a ferramenta:**
    O ponto de entrada da CLI é o arquivo `GASH.py`.
    ```bash
    python3 GASH.py --help
    ```

---

## Estrutura do Projeto

Para facilitar sua navegação, aqui está como organizamos nosso código fonte:

* **`/APIs`**: Contém as integrações e wrappers para comunicação externa (ex: GitHub API). Se você precisa alterar como buscamos dados remotos, mexa aqui.
* **`/Analysis`**: O módulo central de detecção. Aqui reside a lógica que analisa os arquivos YAML em busca dos *smells* configurados.
* **`/Miner`**: Scripts responsáveis pela mineração de repositórios e commits (modos `repo` e `commits` da CLI).
* **`/Utils`**: Funções auxiliares e utilitários compartilhados por todo o projeto.
* **`/Test`**: Testes unitários e de integração. **Toda nova feature deve ter testes correspondentes aqui.**
* **`GASH.py`**: O arquivo principal (Entry Point) que gerencia a CLI e orquestra os módulos.

---

## Como Contribuir

### 1. Reportando Bugs e Sugestões (Issues)
> Antes de codar, verifique as [Issues abertas](https://github.com/mthsfrts/GASH/issues).
- Se for um **Bug**: Inclua passos para reproduzir, prints e o arquivo YAML que causou erro.
- Se for uma **Feature**: Descreva o problema que ela resolve e como você imagina a implementação.
- Sempre verifique se sua Issue contém:
  - Título conciso e resumido.
  - Descrição detalhada.
  - Utilização de labels adequadas.

### 2. Desenvolvimento e Padrões de Código
> Para manter a qualidade e consistência, seguimos estas diretrizes:

* **Estilo Python (PEP 8):** Mantenha o código formatado segundo o [guia de estilo oficial PEP 8](https://peps.python.org/pep-0008/). Recomendamos usar formatadores como `Black` ou `Autopep8` antes de subir.
    ```bash
    pip install black
    black .
    ```
* **Type Hinting:** Sempre que possível, utilize tipagem estática nas assinaturas das funções para facilitar a leitura e manutenção.
    * *Exemplo:* `def analyze_yaml(file_path: str) -> dict:`
* **Docstrings:** Documente classes e funções complexas explicando *o que* fazem e *quais* parâmetros esperam.
* **Modularidade:** Evite funções gigantes em `GASH.py`. Tente delegar a lógica para `Analysis` ou `Utils`.

### 3. Testes
> Não aceitamos código sem testes.
- Certifique-se de que seus testes estão passando localmente antes de abrir o PR.
- Adicione novos casos de teste na pasta `/Test` se você criar uma nova lógica de detecção.

### 4. Melhorar a documentação
> Para garantir que a documentação do projeto reflita precisamente o estado atual do código, é necessário que ela cubra os mais variados aspectos de maneira clara e informativa. Sendo assim, temos como necessário verificar os seguintes aspectos da documentação:
- Ortografia e gramática.
- Clareza e Compreensão.
- Atualização em relação ao código.
- Completude das informações.
- Padronização das informações apresentadas.

---

## Processo de Pull Request (PR)

1. **Antes de [abrir um Pull Request](https://github.com/mthsfrts/GASH/pulls), verifique se:**
    * Existe uma issue vinculada ao seu PR. 
    * Caso não exista, [reporte uma nova issue](#1-reportando-bugs-e-sugestões-issues).
2.  **Crie uma Branch:** Nunca trabalhe direto na branch `prod`. Use nomes descritivos:
    * `feat/novo-detector-smell`
    * `fix/erro-api-github`
    * `docs/atualizacao-readme`
3.  **Commit Semântico:** Escreva mensagens de commit claras, com um resumo descritivo sobre as mudanças.
4.  **Abra o PR:**
    * [Vincule a Issue](https://docs.github.com/pt/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue) que você está resolvendo.
    * Preencha o template do PR descrevendo as mudanças.
5.  **Revisão (Code Review):**
    * Mantenedores revisarão seu código focando em arquitetura, segurança e funcionalidade.
    * Esteja aberto a feedbacks e ajustes. Discussões técnicas acontecem dentro do PR.

---

## Comunicação e Conduta

- Toda comunicação, principalmente a respeito de Issues e/ou Pull Requests, deve ser de fácil acesso aos mantenedores e colaboradores.
- Seja objetivo, tente resumir seu comentário adequadamente.
- Sugestões de melhoria, correções e novas ideias devem sempre ser abertas como Issue antes da implementação.
- Mantenha o respeito e a cortesia. Estamos todos aqui para aprender e construir uma ferramenta melhor.


## Vamos Construir Juntos!

Agradecemos por dedicar seu tempo para ler estas diretrizes e por seu interesse em melhorar o GASH. Sua colaboração é essencial para o sucesso do projeto. Estamos ansiosos para revisar suas contribuições!
