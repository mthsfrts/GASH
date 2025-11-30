# Práticas de Segurança do GASH

Esse documento estabelece práticas de segurança que devem ser seguidas para garantir a confiabilidade e integridade do repositório, contribuidores e usuários.

O objetivo é assegurar a segurança durante todo o desenvolvimento.

---

## 1. Segurança das contas dos trabalhadores
A segurança do projeto começa pela proteção das contas dos colaboradores, já que, se uma conta for comprometida, todo o projeto estará comprometido, o invasor teria acesso a:
- Dados privados;
- Modificação códigos;
- Inserção de malwares nos arquivo.
Comprometendo também a conta de outros contribuidores do projeto.

Logo, para evitar isso é muito importante que os colaboradores se atentem quanto a segurança das próprias contas, por isso recomendamos fortemente:
- Uso da **autenticação de dois fatores (2FA)** do GitHub;
- Não compartilhe, senhas, tokens ou chaves com terceiros;
- Cautela ao usar ambientes inseguros.

Tornando assim a segurança das contas individuais **obrigatória**!

---
## 2. Padrões de Qualidade nos Códigos

Temos o `CONTRIBUITING.md` que define e explica sobre os padrões e qualidade de código, além de também definir como um colaborador deve contribuir com o repositório.

Aqui trataremos sobre a segurança dos códigos, os quais devem cumprir no **mínimo**:
- Usar **tipagem estática** e ser **modular** para  minimizar riscos;
- Evitar ao máximo redundâncias nos códigos;
- O código deve ser mantido simples e claro.

### Sobre os Reviews
 O uso de Pull Requests é obrigatório, e eles serão revisados com base em:
- Estrutura e organização do código;
- Qualidade, clareza e funcionalidade;
- Impacto em toda a arquitetura.
Nada é aprovado sem revisão completa.

---

## 3. Cheque as dependências

É sempre importante verificar as dependências e mantê-las atualizadas para não enfrentar eventuais conflitos.
- As dependências devem ser verificadas constantemente;
- Novas dependências devem ser avaliadas antes de serem adicionadas.

---

## 4. Uso de Branchs
O uso de branches para garantir a segurança do projeto é essencial.
Por isso:
- Nenhum commit deve ser realizado na main;
- Todo código passa por uma revisão;
- O Pull Request deve passar por testes;
- A pipeline CI/CD garante uma segurança passando por verificações antes de ser integrado.

---

## 5. Controle de acessos

Em `GOVERNANCE.md` é explicado sobre a governancia e liderança do projeto.

Ter uma governancia estabelecida é muito importante para a segurança, **evitando alterações indevidas** já que apenas um grupo confiável terá acesso a configurações chaves do repositório.

---

## 6. Report de vulnerabilidades

Caso seja identificado alguma vulnerabilidade que possa por em risco o projeto, é interessante que essa vulnerabilidade seja reportada no privado de um dos nossos colaboradores.

Issues públicas não devem ser abertas, pois possibilita que usuários maliciosos se aproveitem da vulnerabilidade antes de ser corrigida.

Isso deve ser feito para que a vulnerabilidade seja analisada e tratada evitando pôr em risco o projeto.

---

> Pedimos para que todos os contribuidores estejam cientes desses padrões de segurança para garantir um bom andamento do projeto.