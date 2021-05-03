import json
from time import time

from marshmallow import Schema, fields, validates_schema, ValidationError
from marshmallow_oneofschema import OneOfSchema


class Wallet(Schema):
    public_key  = fields.Str(required=True)
    signature   = fields.Str()
    balance     = fields.Int()
    timestamp   = fields.Int()

class Transaction(Schema):
    timestamp =  fields.Int()
    sender    =  fields.Str(required=True)
    receiver  =  fields.Str(required=True)
    amount    =  fields.Int(required=True)
    signature =  fields.Str(required=True)

    class Meta:
        ordered = True


class Block(Schema):
    mined_by = fields.Str(required=False)
    transactions = fields.Nested(Transaction(), many=True)
    height = fields.Int(required=True)
    target = fields.Str(required=True)
    hash = fields.Str(required=True)
    previous_hash = fields.Str(required=True)
    nonce = fields.Str(required=True)
    timestamp = fields.Int(required=True)

    class Meta:
        ordered = True

    @validates_schema
    def validate_hash(self, data, **kwargs):
        block = data.copy()
        block.pop("hash")

        if data["hash"] != json.dumps(block, sort_keys=True):
            raise ValidationError("Fraudulent block: hash is wrong")


class Cliente(Schema):
    ip = fields.Str(required=True)
    port = fields.Int(required=True)





class Ping(Schema):
    pass




