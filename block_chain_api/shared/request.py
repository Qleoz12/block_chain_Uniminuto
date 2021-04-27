from marshmallow import Schema, fields, post_load
from marshmallow_oneofschema import OneOfSchema


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


class MessageDisambiguation(OneOfSchema):
    type_field = "name"
    type_schemas = {
        "ping": PingMessage,
        "peers": PeersMessage,
        "block": BlockMessage,
        "transaction": TransactionMessage,
    }

    def get_obj_type(self, obj):
        if isinstance(obj, dict):
            return obj.get("name")


class MetaSchema(Schema):
    address = fields.Nested(Peer)
    client = fields.Str()


class BaseSchema(Schema):
    meta = fields.Nested(MetaSchema())
    message = fields.Nested(MessageDisambiguation)


def meta(ip, port, version="funcoin-0.1"):
    return {
        "client": version,
        "address": {"ip": ip, "port": port},
    }
