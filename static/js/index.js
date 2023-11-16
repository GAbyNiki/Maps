// This sample uses the Places Autocomplete widget to:
// 1. Help the user select a place
// 2. Retrieve the address components associated with that place
// 3. Populate the form fields with those address components.
// This sample requires the Places library, Maps JavaScript API.
// Include the libraries=places parameter when you first load the API.
// For example: <script
// src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">
let autocomplete;
let address1Field;
let address2Field;
let postalField;
let departureAutocomplete;
let destinationAutocomplete;
let distanceValue;

function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    mapTypeControl: false,
    center: { lat: 0, lng: 0 },
    zoom: 3,
  });

  new AutocompleteDirectionsHandler(map);
}

class AutocompleteDirectionsHandler {
  map;
  originPlaceId;
  destinationPlaceId;
  travelMode;
  directionsService;
  directionsRenderer;
  constructor(map) {
    this.map = map;
    this.originPlaceId = "";
    this.destinationPlaceId = "";
    this.travelMode = google.maps.TravelMode.DRIVING;
    this.directionsService = new google.maps.DirectionsService();
    this.directionsRenderer = new google.maps.DirectionsRenderer();
    this.directionsRenderer.setMap(map);

    const originInput = document.getElementById("origin-input");
    const destinationInput = document.getElementById("destination-input");
    const modeSelector = document.getElementById("mode-selector");
    // Specify just the place data fields that you need.
    const originAutocomplete = new google.maps.places.Autocomplete(
      originInput,
      { fields: ["place_id"] },
    );
    // Specify just the place data fields that you need.
    const destinationAutocomplete = new google.maps.places.Autocomplete(
      destinationInput,
      { fields: ["place_id"] },
    );



    this.setupPlaceChangedListener(originAutocomplete, "ORIG");
    this.setupPlaceChangedListener(destinationAutocomplete, "DEST");
    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(originInput);
    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(
      destinationInput,
    );
    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(modeSelector);
  }
  // Sets a listener on a radio button to change the filter type on Places
  // Autocomplete.
  setupClickListener(id, mode) {
    const radioButton = document.getElementById(id);

    radioButton.addEventListener("click", () => {
      this.travelMode = mode;
      this.route();
    });
  }
  setupPlaceChangedListener(autocomplete, mode) {
    autocomplete.bindTo("bounds", this.map);
    autocomplete.addListener("place_changed", () => {
      const place = autocomplete.getPlace();

      if (!place.place_id) {
        window.alert("Please select an option from the dropdown list.");
        return;
      }

      if (mode === "ORIG") {
        this.originPlaceId = place.place_id;
      } else {
        this.destinationPlaceId = place.place_id;
      }

      this.route();
    });
  }
  route() {
    if (!this.originPlaceId || !this.destinationPlaceId) {
      return;
    }
  
    const me = this;
  
    this.directionsService.route(
      {
        origin: { placeId: this.originPlaceId },
        destination: { placeId: this.destinationPlaceId },
        travelMode: this.travelMode,
      },
      (response, status) => {
        if (status === "OK") {
          me.directionsRenderer.setDirections(response);
  
          // Récupérez la distance du trajet et affichez-la
          const distance = me.extractDistance(response);
          console.log("Distance du trajet :", distance);

          distanceValue = parseFloat(distance.replace(' km', ''));
          // Envoi de la distance au serveur Flask via REST
          console.log("Distance du trajet :", distanceValue);
        }
      },
    );
  }

  extractDistance(response) {
    if (response && response.routes && response.routes[0] && response.routes[0].legs && response.routes[0].legs[0]) {
      return response.routes[0].legs[0].distance.text;
    } else {
      return 'Distance inconnue';
    }
  }
}


initMap()

document.getElementById('calculation-form').addEventListener('submit', function (e) {
  e.preventDefault();  // Empêche la soumission du formulaire par défaut

  // Rassemblez les données du formulaire
  const vitesseMoyenne = document.getElementById('vitesseMoyenne').value;
  const nbDeBorne = document.getElementById('nbDeBorne').value;
  const tempsDeCharge = document.getElementById('tempsDeCharge').value;

  // Créez un objet JSON avec les données du formulaire
  const formData = {
      vitesseMoyenne: vitesseMoyenne,
      nbDeBorne: nbDeBorne,
      tempsDeCharge: tempsDeCharge,
      distance : distanceValue
  };

  // Envoi de la distance convertie au serveur Flask via REST
  fetch('/calculate', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
  })
  .then(response => response.json())
  .then(data => {
      console.log('Réponse du serveur Flask:', data);
      const resultElement = document.getElementById('result');
      resultElement.textContent = `Résultat du calcul : ${data.result} min`;
  })
  .catch(error => {
      console.error('Erreur lors de l\'envoi de la distance au serveur:', error);
  });

});



