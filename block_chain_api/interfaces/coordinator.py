import sys, os
sys.path.append(os.path.abspath('.'))
from block_chain_api.shared.request import BaseSchema, TransactionMessage

import structlog


logger = structlog.getLogger(__name__)

class Coordinator(object):

    def __init__(self):
        self.register=Register(self)
        self.blockchain = Blockchain()
        pass

    def hola(self):
        logger.info("hola")

    def registrarTransaccion(self,tx):

        txmodel=TransactionMessage().make(tx['message']['payload'])
        canregister=self.register.registrarTransaccion(txmodel)
        if canregister:
            #llamar a  bloque
            return "registro tx";
        else:
            return "NO registro tx"

    def checkWallets(self,sender,receiver):

        senderdata,receiverdata=self.blockchain.checkWalletmovement(sender,receiver)
        return senderdata,receiverdata



from .register import Register
from .blockchain import Blockchain
