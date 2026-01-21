## Contribuindo com o Projeto GASH

Primeiramente, agradecemos por dedicar-se a colaborar com o projeto GASH - **The GitHub Actions Smell Hunter**! O objetivo deste documento é definir um conjunto de boas práticas e processos para lhe auxiliar na manutenibilidade do projeto.

### Existem várias maneiras de contribuir:

- Reportar bugs ou solicitar novas funcionalidades através de Issues.
- Resolver issues abertas no código existente. 
- Melhorar a documentação.
- Sugerir refatorações e melhorias de performance.

Seja qual for a forma escolhida, por favor, seja atencioso e respeite nosso código de conduta.

---

## Comunicação

- Toda comunicação, principalmente a respeito de Issues e/ou Pull Requests, deve ser de fácil acesso aos mantenedores e colaboradores.
- Respeito sempre! Não utilize linguagem ofensiva ou grosseira.
- Seja objetivo, tente resumir seu comentário adequadamente.
- Sugestões de melhoria, correções e novas ideias devem sempre ser abertas como Issue antes da implementação.

---

## Issues

> Antes de abrir uma Issue, verifique se:
- O problema/sugestão já foi lançado em Issues.
- Caso não exista, [abra a issue](https://github.com/mthsfrts/GASH/issues/new) contendo:
  - Título conciso e resumido.
  - Descrição detalhada.
  - Prints (se for um bug).
  - Utilização de labels adequadas.

---

## Pull Requests

> Antes de [abrir um Pull Request](https://github.com/mthsfrts/GASH/pulls), verifique se:
- Existe uma issue vinculada ao seu PR.
- Inclua um resumo descritivo sobre as mudanças.
- Desenvolva recursos em uma branch - não trabalhe na branch _prod_.
- Marque a issue vinculada com as palavras-chave, encontradas em [linking-a-pull-request-to-an-issue](https://docs.github.com/pt/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue).

---

## Testes e Verificações

### Código

> Antes de submeter um código ou Pull Request (PR), verificações de qualidade e testes devem ser executados para garantir que o código enviado não comprometa a integridade do projeto. A seguir, os principais requisitos de testes e verificações que devem ser realizados em cada PR:
- **_Estilo e Formatação_**: indentação correta e declaração adequada de funções e variáveis.
- **_Performance (Efetividade e Eficiência)_**: checar funcionalidade do código e verificar se há possíveis gargalos na performance.
- **_Segurança_**: revisão de código, autenticação e controle de acesso, e proteção contra vulnerabilidades.

### Documentação

> Para garantir que a documentação do projeto reflita precisamente o estado atual do código, é necessário que ela cubra os mais variados aspectos de maneira clara e informativa. Sendo assim, temos como necessário verificar os seguintes aspectos da documentação:
- Ortografia e gramática.
- Clareza e Compreensão.
- Atualização em relação ao código.
- Completude das informações.
- Padronização das informações apresentadas.

---

## Padrão de código

> Um padrão de códigos é muito importante para a facilidade de contribuição de muitos mantenedores, pois como muito bem citado anteriormente, a não clareza de um código pode atrasar os objetivos do grupo. Logo, devemos ter clareza e organização nos códigos. Essa boa prática ajuda a manter a consistência e a fluidez do projeto, diminuindo a chance de erros no desenvolvimento do projeto.
Os seguintes critérios devem ser cumpridos:

- **_Código bem estruturado_**: os blocos de código devem ser bem consistentes e seguir um fluxo lógico facilitando a compreensão do código.
- **_Código legível_**: utilizar espaçamento, indentação correta e evitar estruturas complexas, garantindo que qualquer colaborador facilmente entenda o que está sendo feito.
- **_Nomes precisos_**: a nomenclatura utilizada para variáveis ou funções deve ser clara e condizente com o objetivo dela, contribuindo com a legibilidade do código.
- **_Evitar duplicação_**: utilizar funções já existentes é uma boa prática, evitando a criação de funções repetidas ou que possuam o mesmo objetivo, mantendo um código limpo e organizado.
- **_Tratamento correto de erros_** - mensagens de erro e tratamento dos mesmos devem ser claros.
- **_Uso adequado de comentários_** - comentar a lógica e funções de partes do código pode ajudar a entender o que está sendo feito, porém o cuidado com comentários redundantes ou desnecessários será importante para manter o código limpo.
- **_Evitar fragmentos de código inutilizados_** - variáveis e funções não utilizadas devem ser removidas e evitadas.

---

## Revisão de Código

> É fundamental para a manutenção do projeto que os mantenedores tenham noção de como realizar uma revisão de código, garantindo que o código enviado ao repositório principal seja bem escrito, seguro e alinhado com as diretrizes desta documentação.
### Princípios:

- Toda contribuição deve, ao final, passar por uma revisão antes de se aplicar o merge, garantindo que as alterações não comprometam o projeto.
- Revisores devem manter um tom respeitoso, colaborativo e construtivo, proporcionando uma comunicação saudável, como discutido na seção "Comunicação".
- Não se deve inserir opinião ou estilo pessoal na revisão: o que importa de fato é a qualidade da contribuição.
- Discussões técnicas devem ser registradas diretamente no PR.

### Um revisor deve verificar:

- A corretude do programa.
- A qualidade do código, seguindo os padrões estabelecidos em "Padrão de Código".
- A arquitetura, visando mantê-la alinhada ao design do projeto.
- Os riscos, para evitar problemas de segurança ou de performance.
- A documentação, garantindo que ela está devidamente atualizada e que siga o padrão de documentação definido na seção **Testes e Verificações**.
- Os testes, com o objetivo de manter a validade dos testes e de conferir se há funcionalidades não testadas.

### Quem pode ser um revisor?

- Apenas mantenedores ou contribuidores escolhidos pela liderança do projeto GASH, com certo histórico de contribuições.

---

## Fluxo de Contribuição

Após elencarmos algumas boas práticas isoladas para mantenedores no que diz respeito à contribuição, é importante que tenhamos noção do todo, isto é, de como essas boas práticas se inserem em um fluxo de contribuição.

### Passos para uma contribuição seguindo boas práticas

- Primeiramente, faça um fork do projeto, de forma que seja possível contribuir com novas funcionalidades/correções ao projeto GASH sem comprometer o repositório remoto.
- Crie boas branches, isto é, branches descritivas, e que, além disso, sigam um padrão, visando uma melhor organização das branches e tornando uma possível futura busca mais fácil.
- Siga o padrão de código e os critérios definidos no tópico **Padrão de Código**, buscando facilitar o trabalho dos demais mantenedores em realizar futuras contribuições, tornando o código legível e organizado.
- Ao contribuir ao projeto, lembre-se de seguir as diretrizes desse documento, de forma que a contribuição possa ser aceita.
- Antes de abrir o PR, como visto no tópico **Testes e Verificações**, é importante verificar todos os testes para garantir que não há bugs ocasionados pelas alterações, visando não comprometer a integridade do projeto.
  - Lembre-se de seguir o padrão de PR elencado no tópico **Pull Request**.
  - Também é importante ficar atento aos requisitos de testes e verificações, definidos no tópico **Testes e Verificações**.
- Após isso, é interessante que o contribuidor participe de revisões e faça ajustes, principalmente no que diz respeito às funcionalidades por ele implementadas.

---

## Vamos Construir Juntos!

Agradecemos por dedicar seu tempo para ler estas diretrizes e por seu interesse em melhorar o GASH. Sua colaboração é essencial para o sucesso do projeto. Estamos ansiosos para revisar suas contribuições!