# FastAPI, Docker, and PostgreSQL Project

Este projeto é uma API RESTful completa construída com FastAPI, containerizada com Docker e conectada a um banco de dados PostgreSQL. Ele inclui um sistema de autenticação de usuário baseado em JWT e um cliente de desktop simples feito com Tkinter para interagir com a API.

## ✨ Features

-   **Backend Moderno**: API construída com [FastAPI](https://fastapi.tiangolo.com/), oferecendo alta performance e documentação automática.
-   **Containerização**: Todos os serviços (API, Banco de Dados, pgAdmin) são gerenciados com Docker e Docker Compose para um ambiente de desenvolvimento consistente e fácil de implantar.
-   **Autenticação JWT**: Sistema de login seguro usando JSON Web Tokens para proteger os endpoints.
-   **Banco de Dados Relacional**: Utiliza PostgreSQL para persistência de dados, gerenciado com SQLAlchemy ORM.
-   **Validação de Dados**: Usa Pydantic para validação robusta de dados de entrada e saída.
-   **CRUD Completo**: Operações de Criar, Ler, Atualizar e Deletar para o recurso de usuários.
-   **Cliente Desktop**: Uma interface gráfica simples construída com Tkinter para testar todas as funcionalidades da API.

## 📂 Estrutura do Projeto

```
/app                  # Código fonte principal da aplicação FastAPI
├── api/              # Endpoints da API (routers)
├── core/             # Lógica principal (configuração, banco de dados, segurança)
├── models/           # Modelos do banco de dados (SQLAlchemy)
└── schemas/          # Schemas de validação de dados (Pydantic)
/tkinter_client.py    # Aplicação cliente de desktop
/docker-compose.yml   # Definição dos serviços Docker
/Dockerfile           # Definição da imagem Docker para a API
/.env                 # Arquivo para variáveis de ambiente (deve ser criado)
/requirements.txt     # Dependências Python do backend
```

## 🚀 Como Rodar o Projeto

### Pré-requisitos

-   [Docker](https://www.docker.com/get-started)
-   [Docker Compose](https://docs.docker.com/compose/install/)
-   [Python 3.x](https://www.python.org/downloads/) (para rodar o cliente Tkinter localmente)

### Passo 1: Configurar Variáveis de Ambiente

1.  Crie um arquivo chamado `.env` na raiz do projeto.
2.  Copie e cole o conteúdo abaixo no arquivo `.env`, substituindo os valores conforme necessário.

    ```ini
    # Configurações do PostgreSQL
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=supersecretpassword
    POSTGRES_DB=fastapi_db

    # URL de Conexão para o SQLAlchemy (não altere o host 'db')
    DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}

    # Configurações do JWT
    # Gere uma chave segura com: openssl rand -hex 32
    SECRET_KEY=c8a3c6a2b7e1f0d9a3c6a2b7e1f0d9a3c6a2b7e1f0d9a3c6a2b7e1f0d9
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

### Passo 2: Construir e Iniciar os Containers

1.  Abra um terminal na raiz do projeto.
2.  Execute o seguinte comando para construir as imagens e iniciar os containers:

    ```bash
    docker-compose up --build
    ```
    *Para rodar em segundo plano, adicione a flag `-d`.*

### Passo 3: Acessar os Serviços

-   **Documentação da API (Swagger UI)**: Abra seu navegador e acesse `http://localhost:8000/docs`.
-   **pgAdmin (Gerenciador de Banco de Dados)**: Acesse `http://localhost:5050`.
    -   **Email**: `admin@domain.com`
    -   **Senha**: `admin`
    -   Para conectar ao banco de dados dentro do pgAdmin, use `db` como **Host name/address** e as credenciais do seu arquivo `.env`.

## 🖥️ Como Rodar o Cliente Tkinter

O cliente Tkinter roda na sua máquina local, fora do Docker.

### Passo 1: Instalar Dependências

Abra um novo terminal e instale a biblioteca `requests`:

```bash
pip install requests
```

### Passo 2: Executar o Cliente

No mesmo terminal, na raiz do projeto, execute o script:

```bash
python tkinter_client.py
```

Uma janela irá aparecer, permitindo que você crie usuários, faça login e teste todas as operações de CRUD da API.