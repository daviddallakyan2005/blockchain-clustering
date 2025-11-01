import sys
import requests
import json

addr_set = set([sys.argv[1]])
target_addr = sys.argv[1]

def signed_by_addr(tx, addr):
    # Check if any input addresses are in our address set
    try:
        tx_addrs = [x['addr'] for x in [y['prev_out'] for y in tx['inputs']]]
        return any([x in tx_addrs for x in addr])
    except KeyError:
        return False

def cluster(addr):
    url = 'https://blockchain.info/multiaddr?n=100&active=' + "|".join(addr)
    data = requests.get(url)
    result = set()
    incoming = []  # Addresses that sent TO our target
    outgoing = []  # Addresses that received FROM our target

    try:
        data_parsed = data.json()
        txs = data_parsed['txs']

        txs_filtered = list(filter(lambda x: signed_by_addr(x, addr), txs))

        for tx in txs_filtered:
            # Cluster addresses controlled by target
            for inp in tx['inputs']:
                result.add(inp['prev_out']['addr'])
            
            # Collect last addresses that sent to target
            for out in tx['out']:
                out_addr = out.get('addr')
                if out_addr == target_addr:
                    for inp in tx['inputs']:
                        sender = inp['prev_out'].get('addr')
                        if sender and sender not in incoming:
                            incoming.append(sender)
            
            # Collect last addresses that received from target
            for inp in tx['inputs']:
                inp_addr = inp['prev_out'].get('addr')
                if inp_addr == target_addr:
                    for out in tx['out']:
                        receiver = out.get('addr')
                        if receiver and receiver not in outgoing:
                            outgoing.append(receiver)

    except json.decoder.JSONDecodeError:
        result = set(['none'])

    return {
        'clustered_addresses': result,
        'last_10_sent_to_target': incoming[:10],
        'last_10_sent_from_target': outgoing[:10]
    }

if __name__ == "__main__":
    result = cluster(list(addr_set))
    print("Clustered addresses:", result['clustered_addresses'])
    print("Last 10 addresses that sent TO this address:", result['last_10_sent_to_target'])
    print("Last 10 addresses that received FROM this address:", result['last_10_sent_from_target'])
