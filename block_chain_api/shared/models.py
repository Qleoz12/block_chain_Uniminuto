from datetime import datetime


class Ping:
    def __init__(self):
        pass

class WalletModel:
    def __init__(self,public_key, signature=None,timestamp=datetime.utcnow().isoformat(),balance=None):
        self.public_key= public_key
        self.signature = signature
        self.balance = balance
        self.timestamp =timestamp


class TransactionModel:
    def __init__(self,  sender, receiver, signature, timestamp, amount,hash=None):
        self.hash = hash
        self.sender = sender
        self.receiver = receiver
        self.signature = signature # firma de la wallet
        self.timestamp = timestamp
        self.amount = amount

class BlockModel:
    def __init__(
        self,
        mined_by,
        transactions,
        height,
        difficulty,
        hash,
        previous_hash,
        nonce,
        timestamp,
    ):
        self.mined_by = mined_by
        self.transactions = transactions
        self.height = height
        self.difficulty = difficulty
        self.hash = hash
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.timestamp = timestamp

