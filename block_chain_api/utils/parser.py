'''
clase encargada de parsear los json de cada peticion
'''
from marshmallow.exceptions import MarshmallowError, ValidationError

import structlog

from block_chain_api.shared.request import BaseSchema, create_cliente_message, create_transaction_message, \
    create_block_message, Error
from block_chain_api.shared.schema import Block,Ping,Cliente,Transaction

logger = structlog.getLogger(__name__)



class Parser:
    def __init__(self):
        pass

    def parseJson(request):
        try:
            logger.info(request)
            message = BaseSchema().load(request);
            message['error']=Error().load({})
            return message,False
        except ValidationError as error:
            logger.error(error)
            return 'bad request!', True
        except Exception as error:
            logger.error(error)
            return 'bad request!', True




    def handle_message(self, message):
        message_handlers = {
            "block": self.handle_block,
            "ping": self.handle_ping,
            "peers": self.handle_peers,
            "transaction": self.handle_transaction,
        }

        handler = message_handlers.get(message["name"])



    def handle_ping(self, message):
        """
        Executed when we receive a `ping` message
        """
        block_height = message["payload"]["block_height"]

    def handle_transaction(self, message):
        """
        Executed when we receive a transaction that was broadcast by a peer
        """
        logger.info("Received transaction")
        # Validate the transaction
        tx = message["payload"]
        return  create_transaction_message(None,None,tx)


    async def handle_block(self, message):
        """
        Executed when we receive a block that was broadcast by a peer
        """
        logger.info("Received new block")

        block = message["payload"]
        return create_block_message(None,None, block)