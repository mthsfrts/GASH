# Governança do Projeto GASH

O GASH é um projeto open source com foco em **educação e colaboração**, desenvolvido inicialmente em um ambiente acadêmico, mas estruturado para receber contribuições contínuas da comunidade externa.

Este documento explica como o projeto é organizado, quem faz o quê, como as decisões são tomadas e de que forma a comunicação deve acontecer para que o trabalho seja colaborativo e transparente.

---

## 1. Contexto e Objetivos

A governança do GASH visa garantir a saúde e a longevidade do projeto, com os seguintes objetivos centrais:

* **Promover o aprendizado e a Mentoria** contínuos para novos e atuais contribuidores.
* **Deixar claras as responsabilidades** de cada papel, desde Contribuidores até *Maintainers*.
* **Facilitar a entrada de novos membros** da comunidade open-source.
* **Assegurar que as decisões sejam registradas** de forma clara e acessível a qualquer pessoa (*transparência histórica*).

Este documento é um ponto de partida. Ele pode e deve ser ajustado conforme o projeto e a comunidade evoluírem.

---

## 2. Modelo de Governança

O GASH adota um modelo **BDFL Adaptado** (*Benevolent Dictator For Life*), onde a figura central atua como um líder visionário, mas prioriza o consenso da comunidade.

* **Project Lead (BDFL):** [@lincolnrocha]
    * Define a visão de longo prazo e as prioridades estratégicas do projeto.
    * Decide em casos de **impasse** em decisões de arquitetura ou direção.
    * É responsável, junto com os *Maintainers*, pela aprovação final de *merges* na *branch* estável (`prod` / `main`).

* **Core Maintainers (Co-Maintainers):**
    * Ajudam a filtrar *issues* e *Pull Requests* (PRs).
    * Revisam tecnicamente e aprovam PRs.
    * Atuam como **Mentores Técnicos** para os *Feature Teams* (Squads).

A filosofia é sempre buscar o **consenso** e a **colaboração**. A prerrogativa de decisão final do *Project Lead* existe para garantir que o projeto não se paralise em situações de desacordo técnico ou prazos curtos.

---

## 3. Papéis no Projeto

Os nomes dos papéis descrevem as responsabilidades e importam mais do que o *status* acadêmico do indivíduo.

### Project Lead (BDFL)

* Define a direção geral, visão de produto e prioridades estratégicas.
* Dá a palavra final em decisões de maior impacto na arquitetura.
* Chancela *merges* em produção (`prod`/`main`) e grandes *releases*.

### Core Maintainers (Mentores Técnicos / Revisores Chave)

* Acompanham o *backlog* de *issues* e PRs do projeto como um todo.
* **Revisam e aprovam PRs** para a *branch* de integração (`dev`).
* **Orientam** os *Feature Teams* (Squads) em dúvidas de processo, arquitetura e boas práticas.
* Atuam como **mediadores** em divergências técnicas de alto nível.

### Contribuidores (Organizados em Feature Teams / Squads)

O trabalho de desenvolvimento é organizado em *Feature Teams* (Squads). Cada *Team* é responsável por um conjunto de funcionalidades ou módulos.

* **Team Lead (Líder Técnico):**
    * Coordena o trabalho da *Team*.
    * Faz a quebra técnica de *issues* maiores e distribui tarefas.
    * Garante a organização da *branch* do *Team* e faz a ponte com os *Core Maintainers*.
* **Desenvolvedores (Contributors):**
    * Implementam as tarefas de código, aderindo aos padrões de projeto.
* **Technical Reviewer (Revisor de PR do Team):**
    * Faz a primeira revisão técnica de código dentro do *Team*, focando em funcionalidade, testes e padrões.
* **Documentador:**
    * Cria e mantém a documentação (arquivos `.md`, diagramas, documentação de API).
* **QA / Testes:**
    * Cria e mantém suítes de testes, garante a qualidade e segurança do código.

### Contribuidores Externos (Community Contributors)

Contribuidores que não fazem parte do *Feature Team* inicial são bem-vindos. Eles:

* Abem *issues* ou propõem soluções em *issues* existentes.
* Seguem o mesmo fluxo de PRs.
* São acompanhados e *mentorados* pelos **Core Maintainers**.

---

## 4. Branches e Fluxo de Contribuição

O fluxo de *branches* segue o padrão de integração comum:

* `prod` / `main`: *Branch* estável, usada para *releases* em produção.
* `dev`: *Branch* de integração, onde o código aprovado é consolidado.
* *Branches* de *feature*: Criadas a partir de `dev`, ex.: `feature/team-nn-descricao-curta`.

**Fluxo Típico de PR:**

1.  A *Feature* ou *Bugfix* é atribuída a um *Team*.
2.  O *Team* cria uma *branch* de trabalho a partir de `dev`.
3.  O desenvolvimento ocorre, com *commits* pequenos e descritivos.
4.  Ao finalizar, o *Team* abre um PR da *branch* de *feature* para `dev`.
5.  O PR é revisado pelo *Technical Reviewer* do *Team* e, em seguida, por pelo menos um **Core Maintainer**.
6.  Após a aprovação do **Core Maintainer**, o PR é *mergeado* em `dev`.
7.  *Merges* de `dev` para `prod` / `main` são feitos apenas pelos **Project Lead** e **Core Maintainers** em momentos de *release*.

---

## 5. Processo de Decisão

A prioridade é o registro transparente das decisões.

### Decisões de Menor Impacto

Decisões do dia a dia (detalhes de implementação, divisão de tarefas, escopo de *sub-issues*) são tomadas:

* Dentro do próprio **Feature Team**, com o aval do *Team Lead*.
* Com apoio dos **Core Maintainers**, em caso de dúvidas processuais.

Essas decisões devem ser registradas em comentários da *issue* ou PR correspondente.

### Decisões com Divergência Técnica

Quando há divergência técnica e a discussão se arrasta:

1.  A discussão deve ocorrer de forma **respeitosa e técnica** na *issue* ou PR.
2.  Se não houver convergência, um **Core Maintainer** assume a mediação, buscando um consenso.
3.  Se a divergência persistir, o **Project Lead** decide, após ouvir os **Core Maintainers**.

### Decisões de Maior Impacto (Arquitetura e Processo)

Mudanças que afetam o projeto como um todo (arquitetura central, mudança de ferramentas, alteração deste *GOVERNANCE.md*) devem:

* Ter uma *issue* própria (*Proposal Issue*), com contexto e proposta clara.
* Ficar abertas à discussão por um tempo razoável.
* Ser decididas pelo **Project Lead**, com o apoio dos **Core Maintainers**, quando não houver consenso na comunidade.

---

## 6. Evolução de Responsabilidades e Acesso

A ascensão de responsabilidade no GASH é baseada na **consistência** e na **qualidade da contribuição**, não apenas na quantidade de *commits*. Os critérios são:

* Consistência das contribuições (código, testes, documentação).
* Qualidade técnica e adesão a padrões.
* **Postura colaborativa, proatividade** e **Mentoria** a outros membros.
* Disposição em assumir responsabilidade por módulos ou áreas do projeto.

**Caminho de Evolução Típico:**

1.  Começa como **Contributor** em um *Feature Team*.
2.  Evolui para **Technical Reviewer** dentro do *Team*.
3.  Torna-se **Team Lead** ou **Referência Técnica** em um módulo.
4.  Em casos de excelência e comprometimento de longo prazo, pode ser convidado a se tornar um **Core Maintainer**.

Convites para papéis com mais responsabilidade devem ser transparentes e registrados.

---

## 7. Comunicação e Registro de Decisões

A comunicação eficaz é fundamental para a governança.

* **Comunicação Assíncrona (Base):** **Issues** (para bugs, *features* e propostas) e **Pull Requests** (para revisão de código) são os canais primários.
    * **Toda decisão importante deve ser registrada** nesses canais para criar um histórico acessível.
* **Comunicação Síncrona (Apoio):** Canais de *chat* (ex.: Discord) são usados para alinhamentos rápidos, desimpedir discussões travadas ou dúvidas urgentes.
    * **Regra de Ouro:** O resumo do que foi decidido em canais síncronos **deve ser postado de volta** na *issue* ou PR correspondente.

---

## 8. Revisão deste Documento

O `GOVERNANCE.md` é um **documento vivo**.

Propostas de alteração devem ser feitas via PR que modifique este arquivo, associada a uma *Proposal Issue* explicando a motivação da mudança.
