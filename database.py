import sqlite3
from models import Transaction, Block


class BlockchainDB:
    def __init__(self, db_name="blockchain.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        """
        Create the database tables if they do not exist.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocks (
            id INTEGER PRIMARY KEY,
            timestamp REAL,
            data TEXT,
            previous_hash TEXT,
            hash TEXT
        )
        """)
        self.conn.commit()

    def save_block(self, block):
        cursor = self.conn.cursor()
        data = str(block.data) if isinstance(block.data, Transaction) else block.data
        cursor.execute("""
        INSERT INTO blocks (id, timestamp, data, previous_hash, hash)
        VALUES (?, ?, ?, ?, ?)
        """, (block.index, block.timestamp, data, block.previous_hash, block.hash))
        self.conn.commit()

    def load_blockchain(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM blocks ORDER BY id ASC")
        rows = cursor.fetchall()
        chain = []

        for row in rows:
            block_data = row[2]
            if "|" in block_data:  # Heuristic to detect serialized Transaction
                block_data = Transaction.from_string(block_data)

            block = Block(
                index=row[0],
                timestamp=row[1],
                data=block_data,
                previous_hash=row[3],
            )
            block.hash = row[4]
            chain.append(block)

        return chain


    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()
