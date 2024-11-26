import time
from models import Block, Transaction
from database import BlockchainDB


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the current block's hash is valid
            if current_block.hash != current_block.calculate_hash():
                print(f"Block {current_block.index} has been tampered!")
                return False

            # Check if the previous_hash matches the hash of the previous block
            if current_block.previous_hash != previous_block.hash:
                print(f"Block {current_block.index} is not linked to Block {previous_block.index}!")
                return False

        return True

    def add_block(self, transaction):
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.time(), transaction, previous_block.hash)
        self.chain.append(new_block)

    def display_chain(self):
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            if isinstance(block.data, Transaction):
                print(f"Transaction: {block.data}")
            else:
                print(f"Data: {block.data}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            print("-" * 50)


if __name__ == '__main__':
    blockchain = Blockchain()

    # Adding transactions
    blockchain.add_block(Transaction(100, "Alice_Public_Key", "Bob_Public_Key"))
    blockchain.add_block(Transaction(50, "Bob_Public_Key", "Charlie_Public_Key"))
    blockchain.add_block(Transaction(20, "Charlie_Public_Key", "Alice_Public_Key"))

    db = BlockchainDB()

    # Save blocks to database
    for block in blockchain.chain:
        db.save_block(block)

    # Load blockchain from database
    loaded_chain = db.load_blockchain()

    # Use the loaded data in a Blockchain instance
    blockchain.chain = loaded_chain

    # Display the loaded blockchain
    blockchain.display_chain()

    # Validate the loaded blockchain
    print("Is blockchain valid?", blockchain.is_chain_valid())

    # Close the database connection
    db.close()
