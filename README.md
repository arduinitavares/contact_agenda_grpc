# Microsserviço de Agenda de Contactos (gRPC)

Este projeto consiste numa API de microsserviços para uma Agenda de Contactos, desenvolvido com gRPC em Python. A aplicação é gerida com Poetry e desenhada para ser executada em um ambiente de contêiner isolado.

## Tecnologias Utilizadas

- **Python 3.13**
- **gRPC** para comunicação RPC de alta performance.
- **Protocol Buffers** para a definição do contrato da API.
- **Poetry** para a gestão de dependências.
- **Contêineres** (Docker, Apple Container, etc.) para a execução isolada do serviço.

## Estrutura do Projeto

```
contact-agenda-grpc/
│
├── app/                # Código fonte do servidor gRPC
│   ├── __init__.py
│   ├── server.py       # Ponto de entrada do servidor
│   └── service_impl.py # Lógica de negócio do serviço
│
├── client/             # Script de teste para a API
│   ├── __init__.py
│   └── client.py
│
├── proto/              # Definição do contrato da API
│   └── contacts.proto
│
├── .gitignore          # Ficheiros e pastas a ignorar pelo Git
├── Dockerfile          # Instruções para construir a imagem do contêiner
├── pyproject.toml      # Definição do projeto e dependências
├── poetry.lock         # Ficheiro de lock das dependências
└── README.md           # Este ficheiro
```

## Como Executar

Siga os seguintes passos para configurar e executar o projeto.

### 1. Pré-requisitos

- Python 3.13+
- [Poetry](https://python-poetry.org/docs/#installation) instalado.
- Uma ferramenta de contêiner compatível com OCI (ex: Docker, Apple Container).

### 2. Instalação de Dependências

Clone o repositório e instale as dependências com o Poetry:

```bash
poetry install
```

### 3. Construir a Imagem do Contêiner

Use o `Dockerfile` para construir a imagem do serviço:

```bash
# Se usar Docker
docker build -t agenda-service-grpc .

# Se usar Apple Container
container build -t agenda-service-grpc .
```

### 4. Executar o Servidor gRPC

Inicie o contêiner em modo "detached":

```bash
# Se usar Docker
docker run -d --name agenda-grpc-container agenda-service-grpc

# Se usar Apple Container
container run -d --name agenda-grpc-container agenda-service-grpc
```

### 5. Testar a API

O script `client/client.py` é usado para testar as funcionalidades da API.

1.  **Descubra o IP do contêiner:**
    ```bash
    # Se usar Docker
    docker inspect agenda-grpc-container | grep "IPAddress"

    # Se usar Apple Container
    container inspect agenda-grpc-container | grep "IPAddress"
    ```

2.  **Atualize o cliente:**
    Abra o ficheiro `client/client.py` e substitua o endereço no `grpc.insecure_channel()` pelo IP que obteve.

3.  **Execute o cliente:**
    ```bash
    poetry run python -m client.client
    ```

    A saída no terminal irá demonstrar a criação, consulta e listagem dos contactos, confirmando que a API está a funcionar corretamente.
