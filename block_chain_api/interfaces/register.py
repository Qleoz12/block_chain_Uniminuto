from block_chain_api.interfaces.coordinator import Coordinator
from block_chain_api.shared.models import TransactionModel


class Register(object):

    def __init__(self,coordinator):
        self.coordinator=coordinator


    def checkTransaccion(self,tx: TransactionModel):
        '''
        validar transacione provenientes de wallet
        :param tx:
        :return: objeto con validacion y mensaje
        '''
        # validar que ambas direciones existan
        senderValue,receiverValue= self.coordinator.checkWallets(tx.sender, tx.receiver)

        if senderValue and receiverValue:
            return True,senderValue,receiverValue
        else:
            return False,senderValue,receiverValue
