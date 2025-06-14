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

# Instala todas as dependências, incluindo as de desenvolvimento
RUN poetry install --no-root

# Copia a pasta com a definição do protobuf
COPY proto ./proto

# Gera o código gRPC.
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

# Copia o ambiente virtual com as dependências de produção do estágio anterior
COPY --from=builder /app/.venv ./.venv

# Copia o código gerado do estágio anterior
COPY --from=builder /app/contacts_pb2.py .
COPY --from=builder /app/contacts_pb2_grpc.py .

# Copia o código da aplicação
COPY app ./app
COPY client ./client

# Expõe a porta que o servidor gRPC irá usar
EXPOSE 50051

# --- CORREÇÃO AQUI ---
# Define o comando para executar o servidor como um módulo,
# o que garante que os caminhos de importação funcionem corretamente.
CMD [".venv/bin/python", "-m", "app.server"]
