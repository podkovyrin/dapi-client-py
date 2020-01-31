import requests
import json
import random
import datetime
from dapiclient.rpc.jsonrpc.jsonrpc_client import JsonRpcClient

RPC_VERSION = '2.0'
url = 'http://evonet.thephez.com:3000/'
SEED_IP = 'evonet.thephez.com'
SEED_PORT = 3000
MN_LIST_UPDATE_INTERVAL = 60000 / 1000

'''
 * This class holds the valid deterministic masternode list
 * @type {SimplifiedMNListEntry[]}
 * @property {string} proRegTxHash
 * @property {string} confirmedHash
 * @property {string} service - ip and port
 * @property {string} pubKeyOperator - operator public key
 * @property {string} keyIDVoting - public key hash, 20 bytes
 * @property {boolean} isValid
'''
class SimplifiedMNListEntry:
    def __init__(self, seeds, dapi_port = 3000):
        #self.mn_service = set()
        self.mn_entry = []

    def add_entry(self, entry):
        self.mn_entry.append(entry)

    #def add_service(self, service):
    #    self.mn_service.add(service)

    def get_random_masternode(self):
        return random.sample(self.mn_entry, 1)[0]['service']

class MasternodeListProvider:
    def __init__(self, seeds, dapi_port = SEED_PORT):
        if seeds is None:
            seeds = SEED_IP
        if dapi_port is None:
            dapi_port = SEED_PORT

        self.masternode_list = []
        #self.simplified_masternode_list = SimplifiedMNList()
        self.dapi_port = dapi_port
        self.last_update_date = 0
        self.base_block_hash = '0000000000000000000000000000000000000000000000000000000000000000' #constants.masternodeList.NULL_HASH;

    def isEmptyMasternodeList(self):
        return True if len(self.masternode_list.length) == 0 else False


    def get_genesis_hash(self):
        genesis_height = 0
        #node = self.isEmptyMasternodeList() ? sample(self.seeds) : sample(self.masternodeList);
        #ip_address = node.service.split(':')[0];
        ip_address = SEED_IP

        params = { 'height': genesis_height }
        genesis_block_hash = dapi_rpc('getBlockHash', ip_address, self.dapi_port, params)
        return genesis_block_hash

        #return RPCClient.request({
        #  host: ipAddress,
        #  port: this.DAPIPort,
        #}, 'getBlockHash', { height: genesisHeight });



    def update_mn_list(self):
    #if (self.base_block_hash === config.nullHash) {
        self.base_block_hash = self.get_genesis_hash()
        diff = self.get_simplified_mn_list_diff()

        #self.masternode_list = validMasternodesList;
        self.masternode_list = diff['mnList']
        self.base_block_hash = diff['baseBlockHash']
        self.last_update_date = datetime.datetime.utcnow().timestamp()


    def get_simplified_mn_list_diff(self):
        #node = this.isEmptyMasternodeList() ? sample(this.seeds) : sample(this.masternodeList);
        base_block_hash = self.base_block_hash;
        ip_address = SEED_IP #node.service.split(':')[0];

        block_hash = dapi_rpc('getBestBlockHash')

        #const blockHash = await RPCClient.request({
        #  host: ipAddress,
        #  port: this.DAPIPort,
        #}, 'getBestBlockHash', {});
        #if (!blockHash) {
        #  throw new Error(`Failed to get best block hash for getSimplifiedMNListDiff from node ${ipAddress}`);
        #}

        method = 'getMnListDiff'
        params = {
            'baseBlockHash': base_block_hash,
            'blockHash': block_hash
        }
        diff = dapi_rpc(method, ip_address, SEED_PORT, params)

        #const diff = await RPCClient.request({
        #  host: ipAddress,
        #  port: this.DAPIPort,
        #}, 'getMnListDiff', { baseBlockHash, blockHash });
        #if (!diff) {
        #  throw new Error(`Failed to get mn diff from node ${ipAddress}`);
        #}
        return diff


    def needs_update(self):
        time_since_update = datetime.datetime.utcnow().timestamp() - self.last_update_date #MN_LIST_UPDATE_INTERVAL
        #print('Time since update: {}; Limit: {}'.format(time_since_update, MN_LIST_UPDATE_INTERVAL))
        return True if time_since_update > MN_LIST_UPDATE_INTERVAL else False


    def get_mn_list(self):
        if (self.needs_update()):
            #print('Masternode List needs updating...')
            self.update_mn_list()

        return self.masternode_list


def dapi_rpc(method, ip = 'evonet.thephez.com', port = 3000, params = {}, id = 1):
    payload = {
        'jsonrpc': RPC_VERSION,
        'params': params,
        'method': method,
        'id': id
        }

    u = 'http://{}:{}'.format(ip, port)

    headers = {'content-type': 'application/json'}

    try:
        response = requests.post(u, data=json.dumps(payload), headers=headers, timeout=1)
        response.raise_for_status()

        parsed = json.loads(response.text)
        #print('{} response:\n{}\n\n'.format(method, json.dumps(parsed, indent=4, sort_keys=True)))
        return parsed['result']

    except Exception as ex:
        #print('Exception for {} - {}'.format(ip, payload))
        raise

#def check_masternode(ip):
#    try:
#        current_block_hash = dapi_rpc('getBestBlockHash', ip, 3000)
#        print('Success from {}:\t{}'.format(ip, current_block_hash))
#    except Exception as ex:
#        print('Failure from {}:\t** {} **'.format(ip, ex))
#
# def get_masternode_list():
#     params = { 'height': 0 }
#     genesis_block_hash = dapi_rpc('getBlockHash', SEED_IP, SEED_PORT, params)
#
#     current_block_hash = dapi_rpc('getBestBlockHash')
#
#     method = 'getBlockHeaders'
#     params = { 'offset': 1, 'limit': 1 }
#     dapi_rpc(method, SEED_IP, SEED_PORT, params)
#
#     method = 'getMnListDiff'
#     params = {
#         'baseBlockHash': genesis_block_hash,
#         'blockHash': current_block_hash
#     }
#     masternode_list_diff = dapi_rpc(method, SEED_IP, SEED_PORT, params)
#
#     return masternode_list_diff['mnList']

def main():
    #masternode_list = get_masternode_list()

    #mnl = SimplifiedMNListEntry(None)
    #print('Masternode list contain {} masternodes'.format(len(masternode_list)))

    #for mn in masternode_list:
    #    mnl.add_entry(mn)

    #random_mn = mnl.get_random_masternode()
    #print('Random MN: {}'.format(random_mn))

    #for m in mnl.mn_entry:
    #    check_masternode(m['service'].split(':')[0])
    return

if __name__ == "__main__":
    main()