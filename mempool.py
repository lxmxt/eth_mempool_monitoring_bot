import time
from web3 import Web3
from web3.exceptions import TransactionNotFound

# Replace the following with your own Ethereum node's URL (e.g., Infura)
eth_node_url = "https://mainnet.infura.io/v3/aa7b781e38434d9289983fc70362a40a"

# Connect to the Ethereum node
w3 = Web3(Web3.HTTPProvider(eth_node_url))

def get_mempool_transactions(min_value_eth=100):
    # Get the latest pending block
    pending_block = w3.eth.get_block("pending")

    min_value_wei = w3.to_wei(min_value_eth, 'ether')
    filtered_transactions = []

    for tx_hash in pending_block.transactisons:
        try:
            tx = w3.eth.get_transaction(tx_hash)
        except TransactionNotFound:
            print(f"Transaction not found: {tx_hash}")
            continue

        if tx['value'] >= min_value_wei:
            filtered_transactions.append(tx)

    return filtered_transactions

if __name__ == "__main__":
    while True:
        mempool_transactions = get_mempool_transactions()
        if mempool_transactions:
            print("Mempool transactions above 100 ETH:")
            for tx in mempool_transactions:
                print(f"From: {tx['from']}, To: {tx['to']}, Value (ETH): {w3.from_wei(tx['value'], 'ether')}")
        else:
            print("No mempool transactions found above 100 ETH.")
        
        # Wait for a minute before checking again
        time.sleep(30)
