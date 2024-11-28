import json
import os
import time
from models import Block, Transaction
from utils import load_key_from_file


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    # Inside the Blockchain class (is_chain_valid)
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Validate hash
            if current_block.block_hash != current_block.calculate_hash():
                print(f"Block {current_block.index} hash mismatch!")
                return False

            # Validate chain linkage
            if current_block.previous_hash != previous_block.block_hash:
                print(f"Block {current_block.index} linkage mismatch!")
                print(f"current_block_previous_hash {current_block.previous_hash}")
                print(f"previous_block_hash {previous_block.block_hash}")
                return False

            # Validate transactions
            if isinstance(current_block.data, Transaction):
                if not current_block.data.verify_transaction():
                    print(f"Block {current_block.index} transaction verification failed!")
                    return False

        return True

    def add_block(self, transaction):
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.time(), transaction, previous_block.block_hash)
        self.chain.append(new_block)

    def to_dict(self):
        # Convert the blockchain into a dictionary format
        return {
            "chain": [block.to_dict() for block in self.chain]
        }

    def display_chain(self):
        for block in self.chain:
            print(block.to_dict(from_json=True))

    @staticmethod
    def from_dict(data):
        # Deserialize from dictionary to recreate the blockchain and its blocks
        blockchain = Blockchain()

        for block_data in data['chain']:
            # Extracting the block data
            index = block_data['index']
            timestamp = block_data['timestamp']
            previous_hash = block_data['previous_hash']
            block_hash = block_data['block_hash']
            data = block_data['data']  # This is where the transaction details are stored

            # Deserialize transaction data
            if isinstance(data, dict):
                amount = data.get('amount')
                sender_public_key = data.get('sender_public_key')
                receiver_public_key = data.get('receiver_public_key')
                signature = data.get('signature')

                # Create a transaction object with the data
                transaction = Transaction(amount, sender_public_key, receiver_public_key)
                transaction.signature = signature
            else:
                # Handle other cases (e.g., if data is just a string in the genesis block)
                transaction = None

            # Add block to the blockchain
            print(block_hash)
            block = Block(index, timestamp, data=transaction, previous_hash=previous_hash, block_hash=block_hash)
            #blockchain.add_block(block)
            blockchain.chain.append(block)

        return blockchain

    @classmethod
    def save_blockchain_to_json(cls, blockchain, file_path):
        # Save the blockchain as a JSON file
        with open(file_path, 'w') as json_file:
            json.dump(blockchain.to_dict(), json_file, indent=4)

    @staticmethod
    def load_blockchain_from_json(file_path):
        # Load a blockchain from a JSON file
        if os.path.exists(file_path):
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                return Blockchain.from_dict(data)
        else:
            print(f"File {file_path} does not exist.")
            return Blockchain()  # Return an empty blockchain if the file doesn't exist


if __name__ == '__main__':
    # Directory where keys are stored
    base_directory = r'./users/'  # Adjust to the correct directory

    # Load Alice's private and public keys
    alice_private_key = load_key_from_file(os.path.join(base_directory, 'alice', 'private_key.txt'), is_private=True)
    alice_public_key = load_key_from_file(os.path.join(base_directory, 'alice', 'public_key.txt'), is_private=False)

    # Load Bob's private and public keys
    bob_private_key = load_key_from_file(os.path.join(base_directory, 'bob', 'private_key.txt'), is_private=True)
    bob_public_key = load_key_from_file(os.path.join(base_directory, 'bob', 'public_key.txt'), is_private=False)

    # Load Charlie's private and public keys
    charlie_private_key = load_key_from_file(os.path.join(base_directory, 'charlie', 'private_key.txt'),
                                             is_private=True)
    charlie_public_key = load_key_from_file(os.path.join(base_directory, 'charlie', 'public_key.txt'), is_private=False)

    # Now you can use the loaded keys
    print("Alice's private key:", alice_private_key)
    print("Alice's public key:", alice_public_key)
    print("Bob's private key:", bob_private_key)
    print("Bob's public key:", bob_public_key)
    print("Charlie's private key:", charlie_private_key)
    print("Charlie's public key:", charlie_public_key)

    # Create a transaction
    transaction1 = Transaction(100, alice_public_key, bob_public_key)
    print("Original Transaction:", transaction1)

    # Sign the transaction
    transaction1.sign_transaction(alice_private_key)
    print("Transaction signed successfully.")
    print("Signed Transaction:", transaction1)

    # Create a transaction
    transaction2 = Transaction(50, bob_public_key, charlie_public_key)
    print("Original Transaction:", transaction2)

    # Sign the transaction
    transaction2.sign_transaction(bob_private_key)
    print("Transaction signed successfully.")
    print("Signed Transaction:", transaction2)

    # Create a transaction
    transaction3 = Transaction(20, charlie_public_key, alice_public_key)
    print("Original Transaction:", transaction3)

    # Sign the transaction
    transaction3.sign_transaction(charlie_private_key)
    print("Transaction signed successfully.")
    print("Signed Transaction:", transaction3)

    blockchain = Blockchain()

    # Adding transactions
    blockchain.add_block(transaction1)

    # trying to alter the transaction2 content
    # transaction2.amount = 500

    blockchain.add_block(transaction2)
    blockchain.add_block(transaction3)

    # Save the blockchain to a file
    blockchain.save_blockchain_to_json(blockchain, './blockchain.json')

    # Load the blockchain from a file
    loaded_blockchain = Blockchain.load_blockchain_from_json('./blockchain.json')

    # Display the loaded blockchain
    loaded_blockchain.display_chain()

    # Check if the chain is valid
    #print("Is Chain Valid: ", loaded_blockchain.is_chain_valid())
