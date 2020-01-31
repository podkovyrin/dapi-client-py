
class JsonRpcClient:
    def __init__(self):
        return

    def request(self, url, method, params = {}, options = {}):
        destination = 'http://{}:{}'.format(url['host'], url['port'])

        payload = {
            'jsonrpc': RPC_VERSION,
            'method': method,
            'params': params,
            'id': id
            }

        headers = {'content-type': 'application/json'}

        try:
            response = requests.post(destination, data=json.dumps(payload), headers=headers, timeout=1)
            response.raise_for_status()

            parsed = json.loads(response.text)
            #print('{} response:\n{}\n\n'.format(method, json.dumps(parsed, indent=4, sort_keys=True)))
            return parsed['result']

        except Exception as ex:
            #print('Exception for {} - {}'.format(ip, payload))
            raise