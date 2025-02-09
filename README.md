# microservice-fiap-hack-authentication

Este projeto visa autenticar e criar usuarios. Possui uma arquitetura hexagonal em formato de microserviço.

## Pré-Requisitos

Neste projeto há uma necessidade de ter

- Instância do Posgresql;
- Python 3.12;

Crie um arquivo .env na raiz da pasta. O arquivo .env deve estar neste formato. (Favor colocar todas as variáveis sensíveis nos seus devidos lugares)

```
CONNECT_STRING=
PORT=
EXP_DATE=
BASE_URL =
SALT_KEY =
EMAIL_HOST =
EMAIL_PORT =
EMAIL_USER =
EMAIL_PASSWORD =
EMAIL_FROM =
EXP_SERIALIZER=
```

## Documentação da API

#### Criacao de um usuario

```http
  POST /user/create
```

| Parâmetro    | Tipo     | Descrição                                                               |
| :----------- | :------- | :---------------------------------------------------------------------- |
| `user_email` | `string` | **Obrigatório**. email para que o usuario gostaria de se registrar      |
| `password`   | `string` | **Obrigatório**. password o qual o usuario gostaria de se autenticar    |
| `phone`      | `string` | **Obrigatório**. outro meio o qual o usuario gostaria de ser contactado |

#### Retorno

| Parâmetro | Tipo     | Descrição    |
| :-------- | :------- | :----------- |
| `message` | `string` | User created |

#### Exemplo de envio

```
{
    "user_email":"test@xmail.com",
    "password":"dev123",
    "phone":"+5511912347896
}
```

#### Verificacao do Email

Ao receber pelo email um link para validacao do usuario. O usuario ira clicar sendo direcionado para uma pagina e assim verificando a autenticidade do email.

```http
  GET /user/verify/<token>
```

#### Retorno

| Parâmetro | Tipo     | Descrição                    |
| :-------- | :------- | :--------------------------- |
| `message` | `string` | Email verified successfully! |

#### Autenticacao do usuario

```http
  POST /auth/check
```

| Parâmetro    | Tipo     | Descrição                                                            |
| :----------- | :------- | :------------------------------------------------------------------- |
| `user_email` | `string` | **Obrigatório**. email para que o usuario gostaria de se registrar   |
| `password`   | `string` | **Obrigatório**. password o qual o usuario gostaria de se autenticar |

#### Retorno

| Parâmetro | Tipo     | Descrição            |
| :-------- | :------- | :------------------- |
| `token`   | `string` | token formato base64 |

#### Exemplo de envio

```
{
    "user_email":"test@xmail.com",
    "password":"dev123"
}
```

#### Validacao do Token

```http
  POST /auth/verify
```

| Parâmetro | Tipo     | Descrição                                                                                                      |
| :-------- | :------- | :------------------------------------------------------------------------------------------------------------- |
| `token`   | `string` | **Obrigatório**. validacao do token ao autenticar um usuario (caminho reverso do que foi feito no /auth/check) |

#### Retorno

| Parâmetro    | Tipo     | Descrição                                         |
| :----------- | :------- | :------------------------------------------------ |
| `sub`        | `string` | uuid                                              |
| `user_email` | `string` | email do usuario que foi autenticado              |
| `phone`      | `string` | numero do celular/telefone do usuario autenticado |
| `exp`        | `string` | data de expiracao do token                        |
| `iat`        | `string` | quando o token foi gerado                         |

#### Exemplo de envio

```
{
    "token":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkOTdmYjI0MC1hMTNhLTQ1OTEtOWE3Mi0wNjliZTgyMjU0MWEiLCJ1c2VyX2VtYWlsIjoicGF1bG9jaGF2ZXNtZWlyZWxsZXNAZ21haWwuY29tIiwicGhvbmUiOiIrNTUxMTY1NDk4NzEyIiwiZXhwIjoxNzM5MzAzMzU2LCJpYXQiOjE3Mzg2OTg1NTZ9.ZJXyJ-H0WgMcxbihJtNYXRu1bMSBlUDhfbbxD7DMGjox2DU8Y8Ljd6vUqXh2NypXz1Qtcl1clkuegH1V9d15N5dKjKAG9CFQrI9ObU-UfR72AHk0vlyGiQq2zsUWtktrjp4xaZ7Hih-b1hfb0pS4UTLBq6FozYoa_NOXtQqCWtPzJcsllSbWMQRwCS_bJxEVXAJvK4pVWLYsqx8tT2wz_f7Y50F7ZZ7fGgs4qjngE4nBdEWY9Vujzzme8em7l77hO0WHJDmfjNnY8tr2_m83VDhr41Mz0cWNE6eWjzR2sdr-GftL3KKukCSyjmRqUJ84APQN3QN-t7Rl4xmTCNXo9A"
}
```

#### Recuperacao de senha

```http
  POST /password/recover
```

| Parâmetro    | Tipo     | Descrição                                                                 |
| :----------- | :------- | :------------------------------------------------------------------------ |
| `user_email` | `string` | **Obrigatório**. email do usuario que desenha que sua senha seja alterada |

#### Retorno

| Parâmetro | Tipo     | Descrição           |
| :-------- | :------- | :------------------ |
| `message` | `string` | Recovery email sent |

#### Exemplo de envio

```
{
    "user_email":"test@xmail.com"
}
```

#### Alteracao de senha

```http
  POST /password/reset/<token>
```

| Parâmetro      | Tipo     | Descrição                                                                   |
| :------------- | :------- | :-------------------------------------------------------------------------- |
| `new_password` | `string` | **Obrigatório**. senha a qual deseja que o usuario especifico seja alterada |

#### Retorno

| Parâmetro | Tipo     | Descrição                 |
| :-------- | :------- | :------------------------ |
| `message` | `string` | Password reset successful |

#### Exemplo de envio

```
{
    "new_password":"test123"
}
```

## Instalação

Crie um ambiente virtual com python na pasta do repositório

```
  python -m venv venv
```

Selecione o projeto

Linux

```
  source ./venv/bin/activate
```

Windows

```
  .\venv\Scripts\activate
```

Instale as bibliotecas

```
  pip install -r requirements.txt
```

Execute o servidor

```
  python server.py
```

Para rodar os testes unitários, rode o seguinte comando

```
  pytest --cov=src tests/unit
```

Para rodar os testes de comportamento, rode o seguinte comando

```
  behave tests/features
```

## Estrutura do Projeto

```
.gitignore
Dockerfile
generate_keys.py
requirements.txt
server.py
.env
.github
└── workflows
    ├── cd.yml
    └── ci.yml
tests
├── bdd
│   ├── features
│   │   ├── auth_user.feature
│   │   ├── auth_verify.feature
│   │   ├── create_user.feature
│   │   ├── __init__.py
│   │   ├── password_recover.feature
│   │   ├── password_reset.feature
│   │   └── verify_email.feature
│   ├── __init__.py
│   ├── test_auth_user.py
│   ├── test_auth_verify.py
│   ├── test_create_user.py
│   ├── test_password_recover.py
│   ├── test_password_reset.py
│   └── test_verify_email.py
└── unit
    ├── __init__.py
    ├── test_auth_controller.py
    ├── test_auth_service.py
    ├── test_health_controller.py
    ├── test_password_controller.py
    ├── test_user_controller.py
    ├── test_user_repository.py
    └── test_user_service.py
src
├── adapters
│   ├── drivens
│   │   └── infra
│   │       ├── database
│   │       │   ├── config.py
│   │       ├── repositories
│   │       │   └── user_repository.py
│   │       └── settings
│   │           ├── env.py
│   └── drivers
│       └── http
│           ├── controllers
│           │   ├── auth_controller.py
│           │   ├── health_controller.py
│           │   ├── password_controller.py
│           │   └── user_controller.py
│           └── dtos
│               ├── auth_user_dto.py
│               ├── create_user_request_dto.py
│               ├── token_request_dto.py
│               ├── token_response.py
│               └── user_request_dto.py
├── core
│   └── domain
│       ├── application
│       │   ├── ports
│       │   │   └── repositories
│       │   │       ├── Iuser_repository.py
│       │   ├── services
│       │   │   ├── auth_service.py
│       │   │   ├── email_service.py
│       │   │   ├── Iauth_service.py
│       │   │   ├── Iemail_service.py
│       │   │   ├── Iuser_service.py
│       │   │   └── user_service.py
│       │   └── use_cases
│       │       ├── check_auth_use_case.py
│       │       ├── create_user_use_case.py
│       │       ├── dtos
│       │       └── verify_token_use_case.py
│       ├── models
│       │   └── user_model.py
│       └── validators
│           ├── check_auth_request_validator.py
│           ├── create_user_request_validator.py
│           └── token_request_validator.py
├── exceptions.py
└── shared
    ├── logger.py

```
