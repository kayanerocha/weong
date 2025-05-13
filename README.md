
# WeOng

Este projeto tem como objetivo conectar ONGs e voluntários que gostariam de contribuir positivamente com o seu trabalho de forma voluntária. Este sistema está sendo criado para o Trabalho de Conclusão de Curso do curso de Ciência da Computação pela Universidade Paulista.

## Apresentação em Vídeo

A apresentação desse projeto pode ser acessada em: https://drive.google.com/file/d/1xJiKZBULdZC8UjwYYJ28h9X2hVwcRS1V/view?usp=sharing

## Deploy

A aplicação Web deste projeto está hospedada no Render e o banco de dados na AWS por meio do serviço Amazon RDS.

A versão 1 deste projeto pode ser acessada online em [WeOng](https://weong.onrender.com/vagas/).

## Funcionalidades
- Cadastro de ONG;
- Cadastro de voluntário;
- Acesso e edição de perfil;
- Listagem de vagas abertas;
- Visualização de mapa de ONGs;
- Visualização de métricas do projeto;
- ONGs:
  - Cadastro, visualização, edição e exclusão de vaga;
  - Listagem de candidatos;
  - Aprovação/Reprovação de candidato.
- Voluntários:
  - Candidatura à vagas;
  - Cancelamento de candidatura;
  - Visualização de candidaturas.

## Rodando Localmente

Clone o projeto

```bash
  git clone https://github.com/kayanerocha/weong.git
```

Entre no diretório do projeto

```bash
  cd weong
```

Crie o ambiente virtual

```bash
  python -m venv .venv
```

Ative o ambiente virtual

```bash
  .venv\Scripts\activate
```

Instale as bibliotecas

```bash
  pip install -r requirements.txt
```

### Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env (criar uma cópia do .env.exemple e renomear para .env)

`DB_HOST`

`DB_NAME`

`DB_USER`

`DB_PASSWORD`

`DB_PORT`

`GEOCODER_API_KEY`

Aplique as migrações (precisa de um banco de dados MySQL chamado weong)

```bash
  python weong\\manage.py migrate
```

Inicie o servidor (pode alterar a porta para uma que esteja disponível)

```bash
  python weong\\manage.py runserver 7000
```

Crie um usuário administrador

```bash
  python weong\\manage.py createsuperuser
```


## Contribuindo

Sempre que for iniciar qualquer desenvolvimento criar uma nova branch com base na branch `develop` e nomear a branch com base no que está sendo feito. Após o desenvolvimento e tudo funcionando fazer o merge com a branch `develop`.

De preferência seguir os padrões explicados no artigo [Padrões e Nomenclaturas no Git](https://www.brunodulcetti.com/padroes-e-nomenclaturas-no-git/).

Comandos úteis:
- Trocar de branch existente: `git checkout nomedabranch`
- Trocar e criar nova branch: `git checkout -b nomedabranch`
- Adicionar alterações: `git add nomearquivo`
- Commitar: `git commit -m 'commit'`
- Subir as alterações: `git push`
- Merge: `git merge nomedabranch`





## Stack Utilizada

**Front-end:** JavaScript, Bootstrap e Chart.js

**Back-end:** Django

## Documentação
A documentação deste projeto pode ser encontrada no arquivo [WeOng - Documentação](<docs/WeOng - Documentacao.pdf>).


## Autores

- [@ellensolv](https://github.com/ellensolv)
- [@HeitorExp](https://github.com/HeitorExp)
- [@kayanerocha](https://github.com/kayanerocha)
- [@nana-marques](https://github.com/nana-marques)
- [@Natan-Souz](https://github.com/Natan-Souz)
- [@prazeresmath](https://github.com/prazeresmath)

