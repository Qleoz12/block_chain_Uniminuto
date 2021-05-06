import sys, os
from datetime import datetime


sys.path.append(os.path.abspath('.'))
import ast
from block_chain_api.utils.parser import Parser
from block_chain_api.shared.request import BaseSchema, TransactionMessage, Error, WalletMessage, BlockMessage,create_transaction_message
from block_chain_api.shared.models import WalletModel, TransactionModel
from block_chain_api.shared.schema import Block

import structlog
logger = structlog.getLogger(__name__)

class Coordinator(object):

    def __init__(self):
        self.register=Register(self)
        self.blockchain = Blockchain()
        self.minero = Minero(self.blockchain)
        pass

    def hola(self):
        logger.info("hola")

    def consultarFondos(self, walletrequest: BaseSchema):
        model = WalletMessage().make(walletrequest['message']['payload'])

        walletData :WalletModel = self.blockchain.checkWallet(model)
        if walletData:
            walletrequest['message']['payload']['balance']=walletData.balance
            return walletrequest
        else:
            walletrequest['error']['message'] = "no se encontro"
            walletrequest['error']['code'] = 400
            return walletrequest

    def wallet_registrar(self, walletrequest: BaseSchema):
        model = WalletMessage().make(walletrequest['message']['payload'])

        walletData :WalletModel = self.blockchain.registerWallet(model)
        if walletData:
            walletrequest['message']['payload']['timestamp']=walletData.timestamp
            return walletrequest
        else:
            walletrequest['error']['message'] = "error en el proceso de registro de wallet"
            walletrequest['error']['code'] = 400
            return walletrequest

    def checkWallets(self, sender, receiver):
        senderWallet=WalletModel(sender)
        receiverWallet=WalletModel(receiver)
        senderWallet  = self.blockchain.checkWallet(senderWallet)
        receiverWallet = self.blockchain.checkWallet(receiverWallet)
        return senderWallet, receiverWallet

    def registrarTransaccion(self,tx: BaseSchema):
        logger.info(tx)
        txmodel=TransactionMessage().make(tx['message']['payload'])
        canregister,sender,receiver=self.register.checkTransaccion(txmodel)

        if not canregister:
            logger.info("fallo de wallets")
            tx['error']['message'] = "alguna de las wallets tiene problemas"
            tx['error']['code'] = 400
            return tx
        #validacion
        if  sender.public_key!="master" and not self.blockchain.calculateBalance(sender)>txmodel.amount:
            logger.info("fallo de montos")
            tx['error']['message'] = "el monto supera los balances"
            tx['error']['code'] = 400
            return tx

        # validacion
        if not self.blockchain.isOpen():
            logger.info("fallo de bloque")
            tx['error']['message'] = "el bloque se encuentra cerrado"
            tx['error']['code'] = 400
            return tx

        if canregister:
            logger.info("registro tx")
            txmodel=self.blockchain.addTransacction(txmodel)
            tx['message']['payload']['index']=txmodel.index
            tx['message']['payload']['timestamp'] = datetime.utcnow().isoformat()
            return tx
        else:
            tx['error']['message'] = "la transaccion no se puede registrar"
            tx['error']['code'] = 400
            return tx

    def minar(self,walletrequest: BaseSchema):

        blockMined= self.minero.minar()
        if not blockMined:
            logger.info("no hay bloques para minar")
            walletrequest['error']['message'] = "no se puede minar en este momento"
            walletrequest['error']['code'] = 400
            return walletrequest

        blockMined["mined_by"]=walletrequest['message']['payload']['public_key']
        self.blockchain.add_block(blockMined)
        #llenado de data
        ip=walletrequest['meta']['address']['ip']
        port=walletrequest['meta']['address']['port']
        payload={
            'sender': 'master',
            'receiver': walletrequest['message']['payload']['public_key'],
            'amount': '10',
            'signature':'',
            'timestamp': ''
        }
        walletrequest['message']['payload']=Block().dumps(blockMined)
        txreaponse=self.registrarTransaccion({"message":{"payload":payload},"error": {"code":0,"message":None}})
        logger.info(txreaponse)
        return walletrequest

    def calcularSaldos(self, walletrequest: BaseSchema):
        balance=0
        wallet = WalletMessage().make(walletrequest['message']['payload'])
        balance=self.blockchain.calculateBalance(wallet)
        walletrequest['message']['payload']['balance']=balance
        return walletrequest


from .register import Register
from .blockchain import Blockchain
from .minero import Minero

