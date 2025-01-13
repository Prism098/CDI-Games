const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs'); // Nodig voor bestandsschrijfbewerkingen
const { MongoClient } = require('mongodb');


// http://localhost:4000/export-data
// MongoDB Configuratie
const username = "ZuydGebruiker";
const password = encodeURIComponent("3258hnajsidfb302914::__!!");
const authDatabase = "ZuydOpenDag";
const databaseName = "ZuydOpenDag";
const collectionName = "scraper";
const uri = `mongodb://${username}:${password}@20.23.170.134:16283/?authSource=${authDatabase}`;

const client = new MongoClient(uri);

const app = express();
const PORT = 4000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Start de server
app.listen(PORT, async () => {
    console.log(`Server running on http://localhost:${PORT}`);
    try {
        await client.connect();
        await client.db(databaseName).command({ ping: 1 });
        console.log('Succesvol verbonden met MongoDB');
    } catch (err) {
        console.error('Kon geen verbinding maken met MongoDB:', err);
    }
});

// Endpoint om data op te slaan in MongoDB
app.post('/save', async (req, res) => {
    try {
        await client.connect();
        const database = client.db(databaseName);
        const collection = database.collection(collectionName);

        const { name, email, status } = req.body;
        const dataToSave = { name, email, status };

        await collection.insertOne(dataToSave);

        console.log('Data succesvol opgeslagen:', dataToSave);
        res.status(201).send('Data succesvol opgeslagen in MongoDB!');
    } catch (err) {
        console.error('Fout bij opslaan in MongoDB:', err);
        res.status(500).send('Er is een fout opgetreden bij het opslaan.');
    } finally {
        await client.close();
    }
});

// Nieuw: Endpoint om data naar een tekstbestand te exporteren
app.get('/export-data', async (req, res) => {
    try {
        await client.connect();
        const database = client.db(databaseName);
        const collection = database.collection(collectionName);

        const allData = await collection.find({}).toArray(); // Haal alle records op

        // Formatteer data naar tekst
        const formattedData = allData.map(doc => JSON.stringify(doc, null, 2)).join('\n\n');

        // Sla op in een bestand
        const filePath = 'exported_data.txt';
        fs.writeFileSync(filePath, formattedData);

        console.log(`Data succesvol geëxporteerd naar ${filePath}`);
        res.status(200).send(`Data succesvol geëxporteerd naar ${filePath}`);
    } catch (err) {
        console.error('Fout bij exporteren van data:', err);
        res.status(500).send('Er is een fout opgetreden bij het exporteren van de data.');
    } finally {
        await client.close();
    }
});