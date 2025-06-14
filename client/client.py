# client/client.py
"""
Script cliente para testar o serviço gRPC de Contactos.

Este cliente demonstra como interagir com a API, executando as operações
de Adicionar, Consultar e Listar contactos.
"""

import logging

import grpc

import contacts_pb2
import contacts_pb2_grpc
from contacts_pb2 import Category, PhoneType

# Nota: estes ficheiros serão gerados a partir do .proto numa fase posterior.


def run_client():
    """Executa uma sequência de chamadas para testar o servidor."""
    logging.basicConfig(level=logging.INFO)
    # Conecta-se ao servidor gRPC. 'localhost:50051' é o endereço onde
    # o nosso servidor estará a escutar.
    with grpc.insecure_channel("192.168.64.3:50051") as channel:
        stub = contacts_pb2_grpc.ContactServiceStub(channel)
        logging.info("--- 1. A Adicionar Contactos ---")
        try:
            # Primeiro contacto
            add_request_maria = contacts_pb2.AddContactRequest(
                name="Maria Silva",
                phones=[
                    contacts_pb2.PhoneNumber(
                        number="911222333", type=contacts_pb2.PhoneType.MOBILE
                    )
                ],
                category=contacts_pb2.Category.PERSONAL,
            )
            maria_contact = stub.AddContact(add_request_maria)
            logging.info(
                "Contacto 'Maria Silva' adicionado com ID: %s", maria_contact.id)

            # Segundo contacto
            add_request_joao = contacts_pb2.AddContactRequest(
                name="João Souza",
                phones=[
                    contacts_pb2.PhoneNumber(
                        number="225444666", type=contacts_pb2.PhoneType.WORK)
                ],
                category=contacts_pb2.Category.BUSINESS,
            )
            joao_contact = stub.AddContact(add_request_joao)
            logging.info(
                "Contacto 'João Souza' adicionado com ID: %s", joao_contact.id)

        except grpc.RpcError as e:
            logging.error("Erro ao adicionar contacto: %s", e.details())
            return

        logging.info("\n--- 2. A Consultar um Contacto (Maria) ---")
        try:
            get_request = contacts_pb2.GetContactRequest(id=maria_contact.id)
            retrieved_contact = stub.GetContact(get_request)
            logging.info("Contacto recuperado:\n%s", retrieved_contact)
        except grpc.RpcError as e:
            logging.error("Erro ao obter contacto: %s - %s",
                          e.code(), e.details())

        logging.info("\n--- 3. A Listar Todos os Contactos ---")
        try:
            list_response = stub.ListContacts(
                contacts_pb2.ListContactsRequest())
            logging.info("Lista de todos os contactos:")
            for contact in list_response.contacts:
                logging.info(" - %s", contact.name)
        except grpc.RpcError as e:
            logging.error("Erro ao listar contactos: %s", e.details())


if __name__ == "__main__":
    run_client()
