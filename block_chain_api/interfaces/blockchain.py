import asyncio
import json
import math
import random
from hashlib import sha256
from time import time
import structlog

from block_chain_api.shared.models import WalletModel, TransactionModel
from block_chain_api.shared.request import TransactionMessage
from block_chain_api.shared.schema import Transaction

logger = structlog.getLogger("blockchain")


class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.target = "0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"

        self.wallets = []
        self.chain.append(self.new_block())

    def new_block(self):
        block = self.create_block(
            height=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.last_block["hash"] if self.last_block else None,
            nonce=format(random.getrandbits(64), "x"),
            target=self.target,
            timestamp=time(),
        )

        return block

    @staticmethod
    def create_block(
            height, transactions, previous_hash, nonce, target, timestamp=None
    ):
        block = {
            "height": height,
            "transactions": Transaction().dump(transactions,many=True),
            "previous_hash": previous_hash,
            "nonce": nonce,
            "target": target,
            "timestamp": timestamp or time(),
        }

        # Get the hash of this new block, and add it to the block
        block_string = json.dumps(block, sort_keys=True).encode()
        block["hash"] = sha256(block_string).hexdigest()
        return block

    @staticmethod
    def hash(block):
        # We ensure the dictionary is sorted or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last block in the chain (if there are blocks)
        return self.chain[-1] if self.chain else None

    def valid_block(self, block):
        # Check if a block's hash is less than the target...
        return block["hash"] < self.target

    def add_block(self, block):
        # TODO: Add proper validation logic here!
        self.pending_transactions=[]
        self.chain.append(block)

    def isOpen(self):
        return len(self.pending_transactions)<4

    def addTransacction(self,tx: TransactionModel):
        tx.index=len(self.pending_transactions)
        self.pending_transactions.append(tx)
        return tx

    def checkWalletmovement(self,sender,receiver):
        flagwallet1=False
        flagwallet2= False

        for wallet in self.wallets:
            if wallet.public_key == sender.public_key:
                flagwallet1=True
                senderdata=wallet
            if wallet.public_key == receiver.public_key:
                flagwallet2=True
                receiverdata=wallet

        if flagwallet1 and flagwallet2:
            return senderdata,receiverdata

        return None,None

    def checkWallet(self,wallettocheck:WalletModel):
        if wallettocheck.public_key == "master":
            return wallettocheck
        for wallet in self.wallets:
            if wallet.public_key == wallettocheck.public_key:
                return wallet


        return None

    def registerWallet(self,wallettoRegister: WalletModel):
        ispresent=False

        if not wallettoRegister.balance:
            wallettoRegister.balance=0

        for wallet in self.wallets:
            if wallet.public_key == wallettoRegister.public_key:
                ispresent=True
                break

        if ispresent:
            logger.info("wallet presente")
            return None

        if not ispresent:
            self.wallets.append(wallettoRegister)
            return wallettoRegister


    def calculateBalance(self,wallet:WalletModel):
        balance = 0
        inicial = 0
        debts = 0
        actives = 0
        wallet = self.checkWallet(wallet)
        if len(self.chain)>0:
            blockbalance=0
            for blockinchain in self.chain:
                blockbalance+=self.calcularBalanceperBlock(wallet,blockinchain)

            balance+=blockbalance;

        #current
        for tx in self.pending_transactions:
            if tx.receiver == wallet.public_key:
                actives += tx.amount
            if tx.sender == wallet.public_key:
                debts += tx.amount

        balance = wallet.balance+balance + actives - debts
        return balance

    def calcularBalanceperBlock(self,wallet:WalletModel,block):
        debts = 0
        actives = 0
        for tx in block['transactions']:
            txmodel=TransactionMessage().make(tx)
            if txmodel.receiver == wallet.public_key:
                actives += tx.amount
            if txmodel.sender == wallet.public_key:
                debts += tx.amount

        balance = actives- debts
        return balance