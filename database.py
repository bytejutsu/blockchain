import sqlite3
from models import Block, Transaction


class BlockchainDB:
    def __init__(self, db_name="blockchain.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS blocks (
                block_index INTEGER PRIMARY KEY,
                timestamp REAL,
                data TEXT,
                previous_hash TEXT,
                hash TEXT
            )
            """)

    def save_block(self, block):
        with self.conn:
            self.conn.execute("""
            INSERT INTO blocks (block_index, timestamp, data, previous_hash, hash)
            VALUES (?, ?, ?, ?, ?)
            """, (block.index, block.timestamp, str(block.data), block.previous_hash, block.hash))

    def load_blockchain(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM blocks ORDER BY block_index ASC")
        rows = cursor.fetchall()
        chain = []

        for row in rows:
            block_index, timestamp, data, previous_hash, hash_value = row

            if block_index == 0:  # Genesis block
                deserialized_data = data
            else:
                if data.startswith("Transaction"):
                    parts = data.strip("Transaction()").split(", ")
                    amount = int(parts[0].split("=")[1])
                    sender = parts[1].split("=")[1]
                    receiver = parts[2].split("=")[1]
                    deserialized_data = Transaction(amount, sender, receiver)
                else:
                    raise ValueError("Unsupported data format")

            block = Block(block_index, timestamp, deserialized_data, previous_hash)
            chain.append(block)

        return chain

    def close(self):
        if self.conn:
            self.conn.close()
