from prompt_toolkit.filters import app
from flask import Flask, jsonify, request

# clase encargada del manejo del blockcain

class Blockcain:
    pass
class RequestEsquema:
    pass

Blockcain

@app.route('/blockchain', methods=['GET'])
def blockChain():
    def blockChain():
        response = {
        "chain":"json del blockcahin",
        "size":"numero de bloques",
        }
        return jsonify(response), 200

'''
se usa post para obtener dto para tener varias propiedades para la creación
'''
@app.route('/transaccion/new', methods=['POST'])
    def transacion_create():
        txRequest = request.get_json()

        try:
            #parseo del json para obtener un objeto valido
            message = RequestEsquema().loads(txRequest)
        except MarshmallowError:
            logger.info("Received unreadable message", peer=writer)
            break
        return jsonify(response), 200