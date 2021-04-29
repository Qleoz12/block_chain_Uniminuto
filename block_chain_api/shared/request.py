from multiprocessing.connection import Client

from marshmallow import Schema, fields, post_load
from marshmallow_oneofschema import OneOfSchema

#from block_chain_api.shared.schema import Cliente, Block, Transaction, Ping

import structlog

from block_chain_api.shared.schema import Cliente, Block, Transaction, Ping

logger = structlog.getLogger(__name__)
'''
clase encargada de manejar los cuerpos de los json
'''

class BlockMessage(Schema):
    payload = fields.Nested(Block)

    @post_load
    def add_name(self, data, **kwargs):
        data["name"] = "block"
        return data


class TransactionMessage(Schema):
    payload = fields.Nested(Transaction)

    @post_load
    def add_name(self, data, **kwargs):
        data["name"] = "transaction"
        return data


class PingMessage(Schema):
    payload = fields.Nested(Ping)

    @post_load
    def add_name(self, data, **kwargs):
        data["name"] = "ping"
        return data


def meta(ip, port, version="funcoin-0.1"):
    return {
        "client": version,
        "address": {"ip": ip, "port": port},
    }

# utils

def create_block_message(external_ip, external_port, block):
    return BaseSchema().dumps(
        {
            "meta": meta(external_ip, external_port),
            "message": {"name": "block", "payload": block},
        }
    )

def create_transaction_message(external_ip, external_port, tx):
    return BaseSchema().dumps(
        {
            "meta": meta(external_ip, external_port),
            "message": {
                "name": "transaction",
                "payload": tx,
            },
        }
    )

def create_ping_message(external_ip, external_port, block_height, peer_count, is_miner):
    return BaseSchema().dumps(
        {
            "meta": meta(external_ip, external_port),
            "message": {
                "name": "ping",
                "payload": {
                    "block_height": block_height,
                    "peer_count": peer_count,
                    "is_miner": is_miner,
                },
            },
        }
    )

def create_cliente_message(external_ip, external_port, clientes):
    return BaseSchema().dumps(
        {
            "meta": meta(external_ip, external_port),
            "message": {"name": "cliente", "payload": clientes},
        }
    )

'''
encargada de parsear
'''
class MessageDisambiguation(OneOfSchema):
    type_field = "name"
    type_schemas = {
        "ping": PingMessage,
        "block": BlockMessage,
        "transaction": TransactionMessage,
    }
    logger.info(OneOfSchema)

    def get_obj_type(self, obj):
        if isinstance(obj, TransactionMessage):
            return "foo"
        elif isinstance(obj, BlockMessage):
            return "bar"
        else:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))


class MetaSchema(Schema):
    address = fields.Nested(Cliente)
    client = fields.Str()


class BaseSchema(Schema):
    meta = fields.Nested(MetaSchema())
    message = fields.Nested(MessageDisambiguation())