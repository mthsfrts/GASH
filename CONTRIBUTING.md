## Contribuindo com o Projeto GASH

> Primeiramente, agradecemos por dedicar-se a colaborar com o projeto GASH - **The Github Actions Smells Hunter!** O objetivo deste documento é definir um conjunto de boas práticas e processos para lhe auxiliar na manutenibilidade do projeto.

---

## Comunicação

> [@carlexandre](https://github.com/carlexandre): "A comunicação é um dos fatores essenciais para um bom funcionamento de um projeto open source. [...] é sempre necessário documentar interações e ideias que deseja colocar em prática."

* Toda comunicação, principalmente a respeito de Issues e/ou Pull Requests devem ser de fácil acesso aos mantenedores e colaboradores.
* Respeito sempre! Não utilize linguagem ofensiva e grosseira.
* Seja objetivo, tente resumir seu comentário adequadamente.
* Sugestões de melhoria, correções e novas ideias devem sempre ser abertas como Issue antes da implementação.

---

## Issues

> [@Dev-Sams1012](https://github.com/Dev-Sams1012): "como abrir issues ( verificando de algo semelhante já foi reportado, e se não, como descrever adequadamente o problema/sugestão )"

> [@aluiziodev](https://github.com/aluiziodev): "Verificar se existe mais de uma Issue que atende a mesma sugestão. Agrupar Issues de mesma categorização (por meio de labels)"

Antes de abrir uma Issue, verifique se:

* O problema/sugestão já foi lançado em Issues.
* Se não for lançada, abra a issue contendo:
    * Título consiso e resumido.
    * Descrição detalhada.
    * Prints ( se for um bug ).
    * Utilização de labels adequadas.

---

## Pull Requests

> [@aluiziodev](https://github.com/aluiziodev): "Sempre linkar um PR a uma Issue. Sempre exigir testes e validações para PRs (Como mencionou o [@carlexandre](https://github.com/carlexandre)). Fechar Issues apenas quando resolvidas e aprovar PRs apenas após revisão."

Antes de abrir um Pull Request, verifique se:

* Existe uma issue vinculada ao seu PR.
* Inclua um resumo descritivo sobre as mudanças.
* Marque a issue vinculada com as palavras-chaves, encontradas em [linking-a-pull-request-to-an-issue](https://docs.github.com/pt/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)

> Pull Requests serão aprovados por uma equipe específica, que cabe aos participantes da issue [#7](https://github.com/mthsfrts/GASH/issues/7) definirem como será tal organização.

---

## Testes e Verificações

### Código

> [@j0nullduarte](https://github.com/j0nullduarte): "É importante que as verificações chequem não só a qualidade do código, mas também o estilo e formatação do mesmo para garantir que ele será melhor compreendido pelos colaboradores do nosso projeto."

> [@j0nullduarte](https://github.com/j0nullduarte): "É crucial averiguarmos a performance do código de maneira que evitemos possíveis gargalos e possamos garantir um funcionamento fluido e estável do projeto. Assim como a segurança para que possamos evitar possíveis vulnerabilidades no código."

Antes de submeter um código ou Pull Request (PR), verificações de qualidade e testes devem ser executados para garantir que o código enviado não comprometa a integridade do projeto. A seguir, os principais requisitos de testes e verificações que devem ser realizados em cada PR:

* Estilo e Formatação: Indentação correta; Declaração Correta de Funções e Variáveis.
* Performance (Efetividade e Eficiência): Checar funcionalidade do código; Verificar se há possíveis gargalos na performance do código.
* Segurança: Revisão de Código; Autenticação e Controle de Acesso; Proteção Contra Vulnerabilidades.

> [@j0nullduarte](https://github.com/j0nullduarte): "de maneira que o fluxo de integração de novos blocos de código flua de maneira segura e rápida evitando futuras complicações."

### Documentação

> [@j0nullduarte](https://github.com/j0nullduarte): "Não se limitando somente ao código, testes e verificações também deveriam ser modelados para averiguar certos aspectos da documentação"

Para garantir que a documentação do projeto reflita precisamente o estado atual do código, é necessário que ela cubra os mais variados aspectos do projeto de maneira clara e informativa. Sendo assim, temos como necessário verificar os seguintes aspectos da documentação:

* Ortografia e gramática
* Clareza e Compreensão
* Atualização em relação ao código
* Completude das informações
* Padronização das informações apresentadas

> [@j0nullduarte](https://github.com/j0nullduarte): "Garantimos dessa forma que a documentação do projeto está bem estruturada, atualizada e padronizada e que ela esteja sincronizada com o projeto, refletindo seu estado atual."

---

## Padrão de código

> [@j0nullduarte](https://github.com/j0nullduarte): "Código padronizado e devidamente indentado facilitará o entendimento de colaboradores ao entrar em contato com diversas partes do projeto."

Um padrão de códigos é muito importante para a facilidade de contribuição de muitos mantenedores, pois como muito bem citado anteriormente, a não clareza de um código pode atrasar os objetivos do grupo. Logo, devemos ter clareza e organização nos códigos. Essa boa prática ajuda a manter a consistência e a fluidez do projeto, diminuindo a chance de erros no desenvolvimento do projeto.

Os seguintes critérios devem ser cumpridos:

* _Código bem estruturado_: os blocos de códigos devem ser bem consistentes e seguir um fluxo lógico facilitando a compreensão do código;
* _Código legível_: utilizar espaçamento, identação corretas e evitar estruturas complexas, garantindo que qualquer colaborador facilmente entenda o que está sendo feito;
* _Nomes precisos_: a nomenclatura utilizadas para variáveis ou funções devem ser claras e condizentes com o objetivo das mesmas, contribuindo com a legibilidade do código;
* _Evitar duplicação_: utilizar das funções já existentes é uma boa prática , evitando a criação de funções repetidas ou que possuem o mesmo objetivo , mantendo um código limpo e organizado;
* _Tratamento correto de erros_ - mensagens de erro e tratamento dos mesmos devem ser claros;
* _Uso adequado de comentários_ - comentar a lógica e funções de partes do código pode ajudar a entender o que está sendo feito, porém o cuidado com comentários redundantes ou desnecessários será importante para manter o código limpo;
* _Evitar fragmentos de código inutilizados_ - variáveis e funções não utilizadas devem ser removidas e evitadas.

---

## Revisão de Código

> [@Gabriel-Tex](https://github.com/Gabriel-Tex): "É fundamental para a manutenção do projeto que os mantenedores tenham noção de como realizar uma revisão de código, garantindo que o código enviado ao repositório principal seja bem escrito, seguro e alinhado com as diretrizes desta documentação."

### Princípios:

* Toda contribuição deve, ao final, passar por uma revisão antes de se aplicar o merge, garantindo que as alterações não comprometam o projeto;
* Revisores devem manter um tom respeitoso, colaborativo e construtivo, proporcionando uma comunicação saudável, como discutido na seção "Comunicação";
* Não se deve inserir opinião ou estilo pessoal na revisão: o que importa de fato é a qualidade da contribuição;
* Discussões técnicas devem ser registradas diretamente no PR.

### Um revisor deve verificar:

* A corretude do programa;
* A qualidade do código, seguindo os padrões estabelecidos em "Padrão de Código";
* A arquitetura, visando mantê-la alinhada ao design do projeto;
* Os riscos, para evitar problemas de segurança ou de performance;
* A documentação, garantindo que elas estão devidamente atualizadas e que seguem o padrão de documentação definido na seção **Testes e Verificações**;
* Os testes, com o fito de manter a validade dos testes e de conferir se há funcionalidades não testadas.

### Quem pode ser um revisor?

* Apenas mantenedores ou contribuidores escolhidos pela liderança do projeto GASH, com certo histórico de contribuições.

---

## Fluxo de Contribuição

> [@Gabriel-Tex](https://github.com/Gabriel-Tex): "Após elencarmos algumas boas práticas isoladas para mantenedores no que diz respeito a contribuição, é importante que tenhamos noção do todo, isto é, de como essas boas práticas se inserem em um fluxo de contribuição."

### Passos para uma contribuição seguindo boas práticas

* Primeiramente, faça um fork do projeto, de forma que seja possível contribuir com novas funcionalidades / correções ao projeto GASH sem comprometer o repositório remoto;
* Crie boas branches, isto é, branches descritivas, e que, além disso, sigam um padrão, visando uma melhor organização das branches e tornando uma possível futura busca mais fácil;
* Siga o padrão de código e os critérios definidos no tópico **Padrão de Código** por [@Vitor-MB](https://github.com/Vitor-MB), buscando facilitar o trabalho dos demais mantenedores em realizar futuras contribuições, tornando o código legível e organizado;
* Ao contribuir ao projeto, lembre-se de seguir as diretrizes desse documento, de forma que a contribuição possa ser aceita;
* Antes de abrir o PR, como visto no tópico **Testes e Verificações**, escrito por [@j0nullduarte](https://github.com/j0nullduarte), é importante verificar todos os testes para garantir que não há bugs ocasionados pelas alterações, visando não comprometer a integridade do projeto;
    * Lembre-se de seguir o padrão de PR elencado no tópico **Pull Request** por [@aluiziodev](https://github.com/aluiziodev);
    * Também é importante ficar atento aos requisitos de testes e verificações, definidos no tópico **Testes e Verificações**.
* Após isso, é interessante que o contribuidor participe de revisões e faça ajustes, principalmente no que diz respeito às funcionalidades por ele implementadas.

---

## Vamos Construir Juntos!

Agradecemos por dedicar seu tempo para ler estas diretrizes e por seu interesse em melhorar o GASH. Sua colaboração é essencial para o sucesso do projeto. Estamos ansiosos para revisar suas contribuições!