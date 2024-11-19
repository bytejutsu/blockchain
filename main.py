import hashlib
import time


class Transaction:
    def __init__(self, amount, sender_public_key, receiver_public_key):
        self.amount = amount
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key

    def __str__(self):
        return f"Transaction(amount={self.amount}, sender={self.sender_public_key}, receiver={self.receiver_public_key})"


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # Now it's a Transaction object
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_content = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_content.encode()).hexdigest()


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
    # Example usage
    blockchain = Blockchain()

    # Creating transactions
    transaction1 = Transaction(100, "Alice_Public_Key", "Bob_Public_Key")
    transaction2 = Transaction(50, "Bob_Public_Key", "Charlie_Public_Key")
    transaction3 = Transaction(20, "Charlie_Public_Key", "Alice_Public_Key")

    # Adding blocks with transactions
    blockchain.add_block(transaction1)
    blockchain.add_block(transaction2)
    blockchain.add_block(transaction3)

    # Display the blockchain
    blockchain.display_chain()

    # Validate the blockchain
    print("Is blockchain valid?", blockchain.is_chain_valid())

    print("Now we are going to try to tamper the blockchain")

    # Tamper with the blockchain
    blockchain.chain[1].data = Transaction(999, "Hacker_Public_Key", "Bob_Public_Key")

    # toggle the following line of code to experiment between a tampered block and a tampered and not linked block
    blockchain.chain[1].hash = blockchain.chain[1].calculate_hash()

    # Revalidate the blockchain
    print("Is blockchain valid after tampering?", blockchain.is_chain_valid())
