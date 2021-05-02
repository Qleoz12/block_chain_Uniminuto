from multiprocessing.connection import Client

from marshmallow import Schema, fields, post_load, pre_load
from marshmallow_oneofschema import OneOfSchema

from block_chain_api.shared.models import TransactionModel, WalletModel

import structlog

from block_chain_api.shared.schema import Cliente, Block, Transaction, Ping,Wallet

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

    def make(self, data, **kwargs):
        return TransactionModel(**data)

class WalletMessage(Schema):
    payload = fields.Nested(Wallet)
    @post_load
    def add_name(self, data, **kwargs):
        data["name"] = "wallet"
        return data

    def make(self, data, **kwargs):
        return WalletModel(**data)


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
        "wallet": WalletMessage,
    }
    logger.info(OneOfSchema)

    def get_obj_type(self, obj):
        if isinstance(obj, dict):
            return obj.get("name")


class MetaSchema(Schema):
    address = fields.Nested(Cliente)
    client = fields.Str()

class Error(Schema):
    message = fields.Str(missing="")
    code = fields.Int(missing=0)


class BaseSchema(Schema):
    meta= fields.Nested(MetaSchema())
    message = fields.Nested(MessageDisambiguation())
    error = fields.Nested(Error(),missing=Error().load({}))
