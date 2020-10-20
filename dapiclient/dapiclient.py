import grpc

import core_pb2
import core_pb2_grpc
import platform_pb2
import platform_pb2_grpc

import cbor2

GRPC_REQUEST_TIMEOUT = 5

# Set up connection
channel = grpc.insecure_channel('34.219.177.88:3010')
stub = platform_pb2_grpc.PlatformStub(channel)
stubCore = core_pb2_grpc.CoreStub(channel)

def get_documents(contract_id, type, options):
    # Get Document
    # contract_id = dpns_contract_id

    document_request = platform_pb2.GetDocumentsRequest()
    document_request.data_contract_id = contract_id
    document_request.document_type = type
    document_request.limit = 2
    # document_request.where = # Requires cbor (found in dapi-client)

    docs = stub.getDocuments(document_request, GRPC_REQUEST_TIMEOUT)
    # print(docs)
    for d in docs.documents:
        print('Document cbor: {}\n'.format(cbor2.loads(d)))


def main():
    dpns_contract_id = 'CVZzFCbz4Rcf2Lmu9mvtC1CmvPukHy5kS2LNtNaBFM2N'

    get_documents(dpns_contract_id, 'domain', 'limit = 2')

if __name__ == "__main__":
    main()
