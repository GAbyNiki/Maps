from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class calcul_temps_de_trajet(ServiceBase):
    @rpc(float, float,float,float, _returns=float)
    def calcul(self, vitesseMoyenne, distance, nbDeBorne, tempsDeCharge):
        calcul = ((distance / vitesseMoyenne)*60.0 + nbDeBorne * tempsDeCharge)
        return calcul

app = Application([calcul_temps_de_trajet], 'calculator',
                  in_protocol=Soap11(validator='lxml'),
                  out_protocol=Soap11())

wsgi_app = WsgiApplication(app)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('localhost', 8000, wsgi_app)
    server.serve_forever()
    