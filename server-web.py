from flask import Flask, request, render_template, jsonify, send_from_directory
import zeep
import json
import subprocess
import requests
from graph import get_vehicle_list

 # Assurez-vous que le nom du fichier est correct

app = Flask(__name__)


class BornesElectriques:
    def __init__(self):
        self.base_url = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/bornes-irve/records"

    def trouver_bornes_proches(self, lat, lng, distance=10):
        parametres = {
            'latitude': lat,
            'longitude': lng,
            'distance': distance  # Rayon de recherche
        }

        try:
            response = requests.get(self.base_url, params=parametres)
            if response.status_code == 200:
                bornes_proches = response.json()
                return bornes_proches
            else:
                print(f"Erreur lors de la requête : {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Erreur réseau : {e}")
            return None

bornes = BornesElectriques()

@app.route('/bornes_proches', methods=['POST'])
def get_bornes_proches():
    data = request.get_json()
    if data and 'latitude' in data and 'longitude' in data:
        latitude = data['latitude']
        longitude = data['longitude']
        
        bornes_proches = bornes.trouver_bornes_proches(latitude, longitude)
        if bornes_proches:
            return jsonify({'bornes_proches': bornes_proches}), 200
        else:
            return jsonify({'message': 'Aucune borne trouvée ou erreur lors de la requête'}), 404
    else:
        return jsonify({'message': 'Coordonnées manquantes'}), 400

@app.route('/')
def index():

    vehicle_data = get_vehicle_list()
    json_data = json.dumps(vehicle_data)
    
    print(f"vehicle_data : {vehicle_data}")
    vehicle_attributes = []
    
    for vehicle in vehicle_data:
        
        
        attributes = {
            'chargetrip_range_best': vehicle['details']['vehicle']['range']['best'],
            'chargetrip_range_worst': vehicle['details']['vehicle']['range']['worst'],
            'make': vehicle['details']['vehicle']['naming']['make'],
            'model': vehicle['details']['vehicle']['naming']['model'],
            'brande': vehicle['details']['vehicle']['media']['brand']['thumbnail_url'],
            'image_url': vehicle['details']['vehicle']['media']['image']['url'],
        }
        vehicle_attributes.append(attributes)
        
        print(f"ID du véhicule : {vehicle['vehicleId']}")
        print(f"Détails du véhicule : {vehicle['details']}")
        
        
    return render_template('index.html', vehicle_attributes=vehicle_attributes)


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    vitesseMoyenne = data.get('vitesseMoyenne')
    nbDeBorne = data.get('nbDeBorne')
    tempsDeCharge = data.get('tempsDeCharge')
    distance = data.get('distance')
    vehicle = data.get('vehicle')
    range = 100
    
    
    for index, value in enumerate(vehicle):
        print(f"Index: {index}, Value: {value}")
    
    # Appel du service SOAP pour effectuer le calcul A + B
    try:
        # Appel du service SOAP pour effectuer le calcul A + B
        client = zeep.Client('http://localhost:8000/?wsdl')
        result = client.service.calcul(vitesseMoyenne, distance, nbDeBorne, tempsDeCharge)
    except Exception as e:
        # Handle the exception, e.g., print it for debugging
        print(f"SOAP call error: {e}")
        result = None

    # Pass the result to the template
    return jsonify({'result': result})





if __name__ == '__main__':
    app.run(debug=True, port=8001)