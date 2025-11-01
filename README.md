Download --> Run in Terminal: python3 bitcoin-address-cluster.py bc1quhruqrghgcca950rvhtrg7cpd7u8k6svpzgzmrjy8xyukacl5lkq0r8l2d(any bitcoin address)

Output:

    print("Clustered addresses:", result['clustered_addresses']) --> Clustered UTXO-s
    
    print("Last 10 addresses that sent TO this address:", result['last_10_sent_to_target']) --> Last 10 addresses that sent TO this address
    
    print("Last 10 addresses that received FROM this address:", result['last_10_sent_from_target']) --> Last 10 addresses that received FROM this address
