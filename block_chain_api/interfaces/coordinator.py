import sys, os
sys.path.append(os.path.abspath('.'))

from block_chain_api.shared.request import BaseSchema, TransactionMessage, Error, WalletMessage
from block_chain_api.shared.models import WalletModel

import structlog
logger = structlog.getLogger(__name__)

class Coordinator(object):

    def __init__(self):
        self.register=Register(self)
        self.blockchain = Blockchain()
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
        receiverWallet=WalletModel(sender)
        senderWallet  = self.blockchain.checkWallet(senderWallet)
        receiverWallet = self.blockchain.checkWallet(receiverWallet)
        return senderWallet, receiverWallet

    def registrarTransaccion(self,tx: BaseSchema):
        txmodel=TransactionMessage().make(tx['message']['payload'])
        canregister,sender,receiver=self.register.checkTransaccion(txmodel)
        #validacion
        if not sender.balance>txmodel.amount:
            canregister=False

        # validacion
        if not self.blockchain.isOpen():
            canregister = False

        if canregister:
            logger.info("registro tx")
            self.blockchain.addTransacction(txmodel)
        else:
            tx['error']['message'] = "la transaccion no se puede registrar"
            tx['error']['code'] = 400
            return tx







from .register import Register
from .blockchain import Blockchain
