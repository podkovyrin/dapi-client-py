import grpc
import cbor2

import platform_pb2
import platform_pb2_grpc

class DAPIClient:
    def __init__(self, stub, GRPC_REQUEST_TIMEOUT = 5):
        self.stub = stub
        self.GRPC_REQUEST_TIMEOUT = GRPC_REQUEST_TIMEOUT

    def get_documents(self, **params):
        document_request = platform_pb2.GetDocumentsRequest()
        if 'data_contract_id' in params:
            document_request.data_contract_id = params['data_contract_id']
        if 'document_type' in params:
            document_request.document_type = params['document_type']
        if 'where' in params:
            document_request.where = params['where']
        if 'order_by' in params:
            document_request.order_by = params['order_by']
        if 'limit' in params:
            document_request.limit = params['limit']
        if 'start_at' in params:
            document_request.start_at = params['start_at']
        if 'start_after' in params:
            document_request.start_after = params['start_after']

        response = self.stub.getDocuments(document_request, self.GRPC_REQUEST_TIMEOUT)
        return response.documents

def main():
    channel = grpc.insecure_channel('34.219.177.88:3010')
    stub = platform_pb2_grpc.PlatformStub(channel)

    client = DAPIClient(stub)
    docs = client.get_documents(
        data_contract_id='CVZzFCbz4Rcf2Lmu9mvtC1CmvPukHy5kS2LNtNaBFM2N',
        document_type='domain',
        limit=2
    )

    for d in docs:
        print('Document cbor: {}\n'.format(cbor2.loads(d)))

if __name__ == "__main__":
    main()
