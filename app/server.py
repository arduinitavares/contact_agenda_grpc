# app/server.py
"""
Ponto de entrada para iniciar o servidor gRPC.

Este script configura e executa o servidor, associando a lógica de
implementação do serviço (ContactServiceImpl) e expondo-o numa porta.
"""

import logging
import sys
import time
from concurrent import futures

import contacts_pb2_grpc
import grpc
# Importa a implementação do serviço.
from service_impl import ContactServiceImpl

# Adiciona o diretório raiz ao path para encontrar os módulos gerados.
# É uma forma de garantir que os imports funcionem, independentemente
# de como o script é executado.
sys.path.append(".")

# Nota: estes ficheiros serão gerados a partir do .proto numa fase posterior.


def serve():
    """Configura e inicia o servidor gRPC."""
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    contacts_pb2_grpc.add_ContactServiceServicer_to_server(
        ContactServiceImpl(), server
    )

    port = "50051"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logging.info("Servidor gRPC em execução na porta %s.", port)

    try:
        # Mantém o servidor em execução.
        while True:
            time.sleep(86400)  # Dorme por um dia.
    except KeyboardInterrupt:
        logging.info("Servidor a ser finalizado.")
        server.stop(0)


if __name__ == "__main__":
    serve()
