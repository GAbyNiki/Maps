// server.js
const { gql } = require('graphql-tag');
const { getVehicleList, exportDataToJson } = require('./static/js/Client.mjs');
const express = require('express');

const app = express();

// Endpoint pour récupérer la liste de véhicules
app.get('/vehicles', async (req, res) => {
  try {
    const vehicleList = await getVehicleList();

    console.log('Véhicules récupérés :', vehicleList);
    res.json(vehicleList);
  } catch (error) {
    res.status(500).json({ error: 'Une erreur s\'est produite lors de la récupération de la liste de véhicules.' });
  }
});

// Endpoint pour exporter les données au format JSON
app.get('/export', async (req, res) => {
  try {
    const jsonData = await exportDataToJson();
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Content-Disposition', 'attachment; filename=data.json');
    res.send(jsonData);
  } catch (error) {
    res.status(500).json({ error: 'Une erreur s\'est produite lors de l\'export des données.' });
  }
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Le serveur est en cours d'exécution sur le port ${PORT}`);
});
