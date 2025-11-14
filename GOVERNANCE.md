# Governança do Projeto GASH

O GASH é um projeto open source com forte caráter educacional. Ele é desenvolvido no contexto da disciplina do professor @lincolnrocha, com participação de alunos, monitores e, futuramente, contribuidores externos.

Este documento explica como o projeto é organizado, quem faz o quê, como as decisões são tomadas e de que forma a comunicação deve acontecer para que o trabalho seja colaborativo e transparente.

---

## 1. Contexto e objetivos

A governança do GASH tem alguns objetivos centrais:

- apoiar o uso do projeto como ferramenta de aprendizado;
- deixar claras as responsabilidades de cada papel;
- facilitar a entrada de novos contribuidores (alunos e externos);
- registrar as decisões de forma que qualquer pessoa consiga entender o histórico.

Este documento é um ponto de partida. Ele pode e deve ser ajustado conforme o projeto, a disciplina e a comunidade evoluirem.

---

## 2. Modelo de governança

O GASH adota um modelo inspirado em BDFL (Benevolent Dictator For Life), adaptado ao contexto da disciplina.

- O professor @lincolnrocha atua como BDFL:
  - define visão e prioridades gerais do projeto
  - decide casos de impasse em decisões importantes
  - é responsável, junto com os monitores, pelos merges em produção

- Os monitores atuam como co-maintainers:
  - ajudam a filtrar issues e PRs
  - revisam e aprovam PRs
  - orientam as squads e fazem a ponte entre professor e alunos

A ideia é sempre buscar consenso. A prerrogativa de decisão final do professor existe para evitar paralisação quando não houver acordo ou quando for preciso decidir em prazos curtos.

---

## 3. Papéis no projeto

### Professor (BDFL)

- Define a direção geral do projeto.
- Dá a palavra final em decisões de maior impacto.
- Chancela merges em produção (`prod`) e marcos importantes.

### Monitores (co-maintainers)

- Acompanham issues e PRs.
- Revisam e aprovam PRs para a branch de desenvolvimento (dev).
- Orientam squads, esclarecem dúvidas de processo e boas práticas.
- Atuam como mediadores quando há opiniões técnicas divergentes.

### Squads

O trabalho é organizado em squads fixas. Cada squad cuida de um conjunto de issues durante o período da disciplina.

Dentro de cada squad, existem alguns papéis principais (que podem ser acumulados, dependendo do tamanho da equipe):

- Líder de squad:
  Coordena o trabalho da squad, quebra issues maiores em sub-issues, ajuda a distribuir tarefas, organiza a branch da squad e faz a ponte com monitores e professor.

- Desenvolvedores:
  Implementam as tarefas de código acordadas pela squad, seguindo os padrões do projeto.

- Revisor de PR:
  Faz a primeira revisão dos PRs da squad, verifica se o código faz o que promete, se não quebra nada e se está de acordo com a issue.

- Documentador:
  Mantém a documentação atualizada (arquivos `.md`, diagramas, notas de release, documentação de API).

- QA / Testes:
  Cria e mantém testes, pensa em cenários de uso, ajuda a garantir qualidade e segurança do código.

Os nomes dos papéis importam menos do que a ideia central: cada pessoa sabe de que parte é responsável e o que se espera dela em cada entrega.

### Contribuidores externos

Contribuidores que não fazem parte da disciplina são bem-vindos. Eles:

- abrem issues ou comentam em issues existentes para discutir propostas
- seguem o mesmo fluxo de PRs
- são acompanhados por monitores e, quando fizer sentido, podem colaborar com squads ou módulos específicos

---

## 4. Branches e fluxo de contribuição

O fluxo de branches pode ser ajustado com o tempo, mas a ideia geral é:

- prod: branch estável, usada para releases e versões em produção
- dev: branch de integração, onde o código aprovado é consolidado antes de ir para prod
- branches de feature, geralmente criadas a partir de dev, por exemplo:  
  feature/squad-nn-descricao-curta

Fluxo típico de trabalho para uma issue:

1. A issue principal é atribuída a uma squad.
2. O líder da squad, com o time, quebra a issue em sub-issues se necessário e define quem faz o que.
3. A squad cria uma branch de trabalho a partir de dev.
4. O desenvolvimento acontece nessa branch, com commits pequenos e descritivos.
5. Ao finalizar, a squad abre um PR da branch de feature para dev.
6. O PR é revisado primeiro dentro da squad (revisor da squad) e depois por pelo menos um monitor.
7. Uma vez aprovado pelo monitor, o PR é mesclado em dev.
8. Em momentos definidos, o professor e os monitores organizam merges de dev para prod.

Inicialmente, merges nas branches principais (dev e prod) são feitos apenas por monitores e pelo professor.  
Alunos podem revisar PRs e são incentivados a fazer isso, mas não realizam merges nessas branches no começo do projeto.

---

## 5. Processo de decisão

### Decisões do dia a dia

Decisões de menor impacto (detalhes de implementação, divisão de tarefas, pequenas mudanças de escopo) são tomadas:

- dentro da própria squad, em diálogo entre líder, devs, revisor, documentador e QA
- com apoio dos monitores, quando houver dúvida

Essas decisões devem ser registradas em comentários de issue ou PR, para que tenhamos histórico.

### Decisões com divergência

Quando houver opiniões técnicas distintas e a discussão ficar travada, o caminho esperado é:

1. A discussão acontece na issue ou no PR, de forma respeitosa, com argumentos técnicos
2. Se não houver convergência, um monitor assume o papel de mediador
3. O monitor ajuda a buscar um meio-termo ou uma solução que seja aceitável para quem está envolvido
4. Se mesmo assim não houver acordo, o professor decide, ouvindo os monitores

### Decisões de maior impacto

Mudanças que afetam o projeto como um todo (arquitetura, ferramentas centrais, mudanças de processo que atingem todas as squads, alteração deste próprio documento) devem:

- ter uma issue própria, com contexto e proposta clara
- ficar abertas por um tempo razoável para comentários (dentro das limitações do calendário da disciplina)
- ser decididas pelo professor, com apoio dos monitores, quando não houver consenso

---

## 6. Evolução de responsabilidades e acesso

A evolução de responsabilidades no GASH não é baseada apenas em quantidade de commits. O que mais conta é a combinação de:

- consistência das contribuições (código, testes, documentação)
- qualidade técnica
- postura colaborativa e respeito ao fluxo definido
- disposição em ajudar outras pessoas e assumir responsabilidade por partes do projeto

Um caminho típico de evolução pode ser:

1. A pessoa começa contribuindo com pequenas tarefas, seguindo o fluxo de issues e PRs
2. Com o tempo, passa a revisar PRs dentro da squad, com acompanhamento de um monitor
3. Depois de mostrar consistência e maturidade técnica, pode se tornar líder de squad ou referência em uma área do código
4. Em alguns casos, pode receber permissões adicionais (por exemplo, para abrir e organizar issues, ou para ajudar em merges sob supervisão)

Convites para assumir papéis com mais responsabilidade devem ser feitos de forma transparente, de preferência registrados em issue ou PR, para que todos entendam os critérios.

---

## 7. Comunicação e registro de decisões

A governança definida aqui depende muito de uma boa organização da comunicação.

### Comunicação assíncrona

A base da comunicação do projeto são:

- issues (para bugs, features, dúvidas e propostas)
- pull requests (para discutir e revisar mudanças de código)

Toda decisão importante deve estar registrada em algum desses lugares.  
Isso evita que informações fiquem perdidas em conversas privadas ou em canais de chat e permite que qualquer pessoa que chegue depois entenda o histórico.

### Comunicação síncrona

Devem existir canais síncronos (por exemplo, um canal específico no Discord) para conversas mais rápidas. A função principal desses canais é destravar discussões que ficaram paradas, fazer alinhamentos pontuais e tirar dúvidas urgentes.

Mesmo quando a conversa acontecer de forma síncrona, vale a seguinte regra:

- o resumo do que foi decidido deve voltar para a issue ou PR correspondente

### Fluxo de comunicação entre papéis

De forma geral:

- o professor define orientação geral, prioridades maiores e valida decisões importantes
- monitores traduzem essas orientações para o dia a dia das squads, acompanham o que está acontecendo e ajudam a resolver problemas
- líderes de squad organizam o trabalho dentro de cada grupo e garantem que as informações circulem
- devs, revisores, documentadores e QA implementam e registram o trabalho

Esse fluxo não é uma hierarquia rígida. Alunos podem e devem trazer sugestões e questionamentos “de baixo para cima”, principalmente via issues.  
O importante é que as informações circulem e fiquem registradas de maneira clara.

---

## 8. Revisão deste documento

O GOVERNANCE.md é um documento vivo.

Ele deve ser revisado:

- para refletir o que funcionou e o que precisa ser ajustado, ou
- sempre que houver mudança relevante na forma como o projeto é organizado.

Propostas de alteração devem ser feitas via PR que modifica este arquivo, associada a uma issue explicando o motivo da mudança.

A governança do GASH é um compromisso coletivo. Ela só faz sentido se for conhecida, aplicada e, quando necessário, revisada pela própria comunidade do projeto.

