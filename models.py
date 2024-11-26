import hashlib


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
        self.data = data  # Can be a string or a Transaction object
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_content = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_content.encode()).hexdigest()
