import sys
sys.path.append("..")
import flask

from prompt_toolkit.filters import app
from flask import Flask, jsonify, request
from utils.parser import Parser
from interfaces.coordinator import Coordinator
import structlog
logger = structlog.getLogger(__name__)
coordinator = Coordinator()

# clase encargada del manejo del blockcain

class Blockcain:
    pass
class RequestEsquema:
    pass




app = flask.Flask(__name__)
app.config["DEBUG"] = True



@app.route('/blockchain', methods=['GET'])
def blockChain():
    response = {
    "chain":"json del blockchain.py",
    "size":"numero de bloques",
        }
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
        return jsonify(txregistrada), 200


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)