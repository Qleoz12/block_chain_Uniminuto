from block_chain_api.interfaces.register import Register


class Coordinator(object):

    def __init__(self):
        self.register=Register()
        pass

    def registrarTransaccion(self,tx):
        canregister=self.register.registrarTransaccion(tx)
        if canregister:
            #llamar a  bloque
            return "registro tx";
        else:
            return "NO registro tx"
