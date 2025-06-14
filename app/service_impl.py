# app/service_impl.py
"""
Implementação da lógica de negócio para o serviço de Contactos.

Esta classe implementa os métodos definidos no ficheiro .proto e manipula
os dados dos contactos, que são armazenados em memória para simplificar.
"""

import uuid
from typing import Dict

import grpc

# Nota: estes ficheiros serão gerados a partir do .proto numa fase posterior.
# O seu editor de código pode assinalá-los como um erro por agora.
import contacts_pb2
import contacts_pb2_grpc


class ContactServiceImpl(contacts_pb2_grpc.ContactServiceServicer):
    """
    Fornece a implementação dos métodos do serviço de Contactos.
    """

    def __init__(self):
        """Inicializa o serviço com um 'banco de dados' em memória."""
        self._contacts: Dict[str, contacts_pb2.Contact] = {}

    def AddContact(self, request, context):
        """Cria e armazena um novo contacto a partir de uma requisição."""
        print(f"Requisição para adicionar o contacto: {request.name}")
        contact_id = str(uuid.uuid4())
        contact = contacts_pb2.Contact(
            id=contact_id,
            name=request.name,
            phones=request.phones,
            category=request.category,
        )
        self._contacts[contact_id] = contact
        print(f"Contacto '{contact.name}' adicionado com o ID: {contact_id}")
        return contact

    def GetContact(self, request, context):
        """Recupera um contacto específico com base no seu ID."""
        print(f"Requisição para consultar o ID: {request.id}")
        contact = self._contacts.get(request.id)

        if contact:
            return contact

        # Se o contacto não for encontrado, informa o cliente através do contexto.
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details(
            f"Contacto com o ID '{request.id}' não encontrado.")
        return contacts_pb2.Contact()

    def ListContacts(self, request, context):
        """Devolve a lista de todos os contactos registados."""
        print("Requisição para listar todos os contactos.")
        return contacts_pb2.ListContactsResponse(
            contacts=list(self._contacts.values())
        )
