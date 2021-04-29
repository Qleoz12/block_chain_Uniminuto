
class Ping:
    def __init__(self):
        pass

class Transaction:
    def __init__(self, hash, sender, receiver, signature, timestamp, amount):
        self.hash = hash
        self.sender = sender
        self.receiver = receiver
        self.signature = signature # firma de la wallet
        self.timestamp = timestamp
        self.amount = amount

class Block:
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

