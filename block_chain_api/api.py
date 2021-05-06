import sys
sys.path.append("..")
import marshmallow
from block_chain_api.shared.request import BlockChainMessage
import flask
import jsbeautifier
from prompt_toolkit.filters import app
from flask import Flask, jsonify, request
from utils.parser import Parser
from interfaces.coordinator import Coordinator

import structlog
logger = structlog.getLogger(__name__)
coordinator = Coordinator()

# clase encargada del manejo del blockcain
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/blockchain', methods=['GET'])
def blockChain():
    opts = jsbeautifier.default_options()
    opts.indent_size = 2

    response = {
    "chain":BlockChainMessage().dumps(coordinator.blockchain),
    "size": len(coordinator.blockchain.chain),
        }

    return jsonify(response), 200

@app.route('/blockchain/minar', methods=['POST'])
def mine():
    txRequest = request.get_json()
    # parseo del json para obtener un objeto valido
    message, error = Parser.parseJson(txRequest)
    if error:
        return message, 400
    # cerrar bloque
    response = coordinator.minar(message)

    if response['error'] \
            and response['error']['code'] != 0:
        return response, response['error']['code']

    return jsonify(response), 200

'''
se usa post para obtener dto para tener varias propiedades para la creación
'''
@app.route('/transaction/new', methods=['POST'])
def transacion_create():
        txRequest = request.get_json()
        #parseo del json para obtener un objeto valido
        message,error = Parser.parseJson(txRequest)

        if error:
            return message,400
        #crear nueva transaccion
        txregistrada=coordinator.registrarTransaccion(message)

        if txregistrada['error'] \
                and message['error']['code']!=0:
            return txregistrada,txregistrada['error']['code']

        return jsonify(txregistrada), 200


@app.route('/wallet/consultarFondos', methods=['POST'])
def wallet_checkFondos():
        requestdata = request.get_json()
        #parseo del json para obtener un objeto valido
        message,error = Parser.parseJson(requestdata)

        if error:
            return message,400
        #crear consulta
        txregistrada=coordinator.calcularSaldos(message)

        if txregistrada['error']\
        and message['error']['code']!=0:
            return txregistrada,txregistrada['error']['code']

        return jsonify(txregistrada), 200

@app.route('/wallet/registrar', methods=['POST'])
def wallet_registrar():
        requestdata = request.get_json()
        #parseo del json para obtener un objeto valido
        message,error = Parser.parseJson(requestdata)

        if error:
            return message,400
        #crear consulta
        message=coordinator.wallet_registrar(message)

        if message['error'] and message['error']['code']!=0:
            return message,message['error']['code']

        return jsonify(message), 200














if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)