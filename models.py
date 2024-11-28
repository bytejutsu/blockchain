import base64
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization


class Transaction:
    def __init__(self, amount, sender_public_key, receiver_public_key):
        self.amount = amount
        self.sender_public_key = sender_public_key  # Public key object
        self.receiver_public_key = receiver_public_key  # Public key object
        self.signature = None

    def sign_transaction(self, private_key):
        """
        Sign the transaction using the sender's private key.
        """
        # Prepare the data to be signed (e.g., amount, sender and receiver public keys)
        message = f"{self.amount}{self.sender_public_key}{self.receiver_public_key}".encode()

        # Sign the message using the private key
        self.signature = private_key.sign(
            message,  # Data to be signed
            padding.PKCS1v15(),  # Padding scheme
            hashes.SHA256()  # Hashing algorithm
        )

        # You could also convert the signature to a more transportable format like base64 or hex if needed.
        # Example: base64.b64encode(self.signature)

    def verify_transaction(self):
        # Add transaction verification logic
        return True

    def to_dict(self):
        """
        Convert the transaction to a dictionary that can be serialized.
        """
        return {
            "amount": self.amount,
            "sender_public_key": self.sender_public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode(),  # Convert to PEM string
            "receiver_public_key": self.receiver_public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode(),  # Convert to PEM string
            "signature": base64.b64encode(self.signature).decode() if self.signature else None,
            ## Base64 encode the signature
            #"signature": self.signature,
        }

    @classmethod
    def from_dict(cls, tx_dict):
        """
        Deserialize a transaction from a dictionary.
        """
        # Convert the PEM string back to public key objects
        sender_public_key = serialization.load_pem_public_key(tx_dict['sender_public_key'].encode())
        receiver_public_key = serialization.load_pem_public_key(tx_dict['receiver_public_key'].encode())

        # Create the transaction object
        transaction = cls(tx_dict['amount'], sender_public_key, receiver_public_key)

        # Decode the base64 signature
        signature = base64.b64decode(tx_dict['signature']) if tx_dict['signature'] else None
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
        content = f"{self.index}|{self.timestamp}|{self.data}|{self.previous_hash}"
        return hashlib.sha256(content.encode()).hexdigest()

    def to_dict(self):
        # Convert the block into a dictionary format
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data.to_dict() if isinstance(self.data, Transaction) else self.data,  # Serialize transaction data
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

    def __str__(self):
        data_str = str(self.data) if isinstance(self.data, Transaction) else self.data
        return f"{self.index}|{self.timestamp}|{data_str}|{self.previous_hash}|{self.hash}"
