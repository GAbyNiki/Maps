import requests
import json

# Define GraphQL queries similar to the original Java file
getVehicleListQuery = '''
query vehicleList($page: Int, $size: Int, $search: String) {
  vehicleList(
    page: $page, 
    size: $size, 
    search: $search
  ) {
    id
    naming {
      make
      model
      chargetrip_version
    }
    media {
      image {
        thumbnail_url
      }
    }
  }
}
'''

getVehicleDetailsQuery = '''
query vehicle($vehicleId: ID!) {
  vehicle(id: $vehicleId) {
    naming {
      make
      model
      chargetrip_version
    }
    media {
      image {
        url
      }
      brand {
        thumbnail_url
      }
    }
    battery {
      usable_kwh
    }
    range {
      best {
        highway
        city
        combined
      }
      worst {
        highway
        city
        combined
      }
      chargetrip_range {
        best
        worst
      }
    }
    routing {
      fast_charging_support
    }
    connectors {
      standard
    }
    performance {
      acceleration
      top_speed
    }
  }
}
'''

headers = {
    'x-client-id': '652661f712e5356e23ce6a9f',
    'x-app-id': '652661f712e5356e23ce6aa1',
}

url = 'https://api.chargetrip.io/graphql'

def create_client():
    return requests.Session()

def get_vehicle_list():
    try:
        client = create_client()
        response = client.post(url, json={'query': getVehicleListQuery}, headers=headers)
        data = response.json().get('data', {}).get('vehicleList', [])

        if data:
            detailed_vehicle_data = []

            for vehicle in data:
                vehicle_id = vehicle.get('id')
                detailed_vehicle = get_vehicle_details(vehicle_id)
                detailed_vehicle_data.append({'vehicleId': vehicle_id, 'details': detailed_vehicle})

            return detailed_vehicle_data
        else:
            print("Aucun véhicule trouvé.")
            return []
    except Exception as e:
        print(e)
        return []

def get_vehicle_details(vehicle_id):
    try:
        client = create_client()
        variables = {'vehicleId': vehicle_id}
        response = client.post(url, json={'query': getVehicleDetailsQuery, 'variables': variables}, headers=headers)
        return response.json().get('data', {})
    except Exception as e:
        print(e)
        return None

def export_data_to_json():
    data = get_vehicle_list()
    json_data = json.dumps(data)
    return json_data

# Example usage
if __name__ == "__main__":
    json_output = export_data_to_json()
    print(json_output)
