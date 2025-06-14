# Dockerfile para um projeto Python com Poetry

# --- Estágio 1: Builder ---
# Este estágio instala todas as dependências (incluindo as de desenvolvimento)
# e gera o código Python a partir do ficheiro .proto.
FROM python:3.13.2-slim as builder

# Define variáveis de ambiente para o Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1

WORKDIR /app

# Instala o Poetry
RUN pip install poetry

# Copia os ficheiros de definição do projeto e de lock
COPY pyproject.toml poetry.lock ./

# Instala todas as dependências, incluindo as de desenvolvimento (--no-root para não instalar o projeto em si)
RUN poetry install --no-root

# Copia a pasta com a definição do protobuf
COPY proto ./proto

# Gera o código gRPC. Ativamos o ambiente virtual do Poetry para usar as ferramentas instaladas.
RUN . .venv/bin/activate && \
    python -m grpc_tools.protoc \
    -I./proto \
    --python_out=. \
    --grpc_python_out=. \
    ./proto/contacts.proto


# --- Estágio 2: Final ---
# Este estágio cria a imagem final e otimizada para produção.
FROM python:3.13.2-slim

WORKDIR /app

# Define as mesmas variáveis de ambiente
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1

# Copia o ambiente virtual com as dependências de produção do estágio anterior
COPY --from=builder /app/.venv ./.venv

# Copia o código gerado do estágio anterior
COPY --from=builder /app/contacts_pb2.py .
COPY --from=builder /app/contacts_pb2_grpc.py .

# Copia o código da aplicação
COPY app ./app

# Expõe a porta que o servidor gRPC irá usar
EXPOSE 50051

# Define o comando para executar o servidor quando o container iniciar
CMD [".venv/bin/python", "app/server.py"]