'''
clase encargada de parsear los json de cada peticion
'''
from marshmallow.exceptions import MarshmallowError
import structlog

class parser
    def __init__(self):
        pass

    def parseJson(self, request):
        try:
            # parseo del json para obtener un objeto valido
            message = RequestEsquema().loads(request)
        except MarshmallowError:
            logger.info("Received unreadable message", peer=writer)
            break