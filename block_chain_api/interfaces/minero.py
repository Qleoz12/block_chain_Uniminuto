import structlog

from block_chain_api.shared.models import BlockModel

logger = structlog.getLogger(__name__)

class Minero(object):

    def __init__(self,blockchain):
        self.blockchain=blockchain

    def minar(self):
        new_block: BlockModel =None
        if self.blockchain.isOpen():
            logger.info(self.blockchain)
            return None

        while not(self.blockchain.isOpen()):
            new_block = self.blockchain.new_block()
            logger.info(new_block)
            if self.blockchain.valid_block(new_block):
                break

        return new_block