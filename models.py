import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization


class Transaction:
    def __init__(self, amount, sender_public_key, receiver_public_key):
        self.amount = amount
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key
        self.signature = None

    def __str__(self):
        """
        Represent the transaction as a simple string.
        """
        sender_pem = self.sender_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()
        receiver_pem = self.receiver_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()
        signature_str = self.signature.hex() if self.signature else ""
        return f"{self.amount}|{sender_pem}|{receiver_pem}|{signature_str}"

    def sign_transaction(self, private_key):
        """
        Sign the transaction using the sender's private key.
        """
        # Serialize the transaction (excluding the signature) for signing
        transaction_data = f"{self.amount},{self.sender_public_key},{self.receiver_public_key}"

        # Generate the signature
        self.signature = private_key.sign(
            transaction_data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256()
        )

    def verify_transaction(self):
        """
        Verify the transaction's signature using the sender's public key.
        """
        if not self.signature:
            raise ValueError("Transaction is not signed.")

        # Serialize the transaction (excluding the signature) for verification
        transaction_data = f"{self.amount},{self.sender_public_key},{self.receiver_public_key}"

        try:
            # Verify the signature
            self.sender_public_key.verify(
                self.signature,
                transaction_data.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False

    @staticmethod
    def from_string(transaction_str):
        """
        Deserialize a string into a Transaction object.
        """
        parts = transaction_str.split("|")
        amount = int(parts[0])
        sender_public_key = serialization.load_pem_public_key(parts[1].encode())
        receiver_public_key = serialization.load_pem_public_key(parts[2].encode())
        signature = bytes.fromhex(parts[3]) if parts[3] else None
        transaction = Transaction(amount, sender_public_key, receiver_public_key)
        transaction.signature = signature
        return transaction


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # Can be a string or a Transaction object
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Calculate the hash of the block using its string representation.
        """
        content = f"{self.index}|{self.timestamp}|{self.data}|{self.previous_hash}"
        return hashlib.sha256(content.encode()).hexdigest()

    def __str__(self):
        """
        Represent the block as a simple string.
        """
        data_str = str(self.data) if isinstance(self.data, Transaction) else self.data
        return f"{self.index}|{self.timestamp}|{data_str}|{self.previous_hash}|{self.hash}"

    @staticmethod
    def from_string(block_str):
        """
        Deserialize a string into a Block object.
        """
        parts = block_str.split("|")
        index = int(parts[0])
        timestamp = parts[1]
        data = (
            Transaction.from_string(parts[2])
            if "," in parts[2]  # A simple check to identify transaction-like data
            else parts[2]
        )
        previous_hash = parts[3]
        hash_value = parts[4]
        block = Block(index, timestamp, data, previous_hash)
        block.hash = hash_value  # Set the hash explicitly
        return block
