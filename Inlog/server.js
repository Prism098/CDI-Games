const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs'); // Nodig voor bestandsschrijfbewerkingen
const { MongoClient } = require('mongodb');

// MongoDB Configuratie
const username = "ZuydGebruiker";
const password = encodeURIComponent("3258hnajsidfb302914::__!!");
const authDatabase = "ZuydOpenDag";
const databaseName = "ZuydOpenDag";
const collectionName = "scraper";
const uri = `mongodb://${username}:${password}@20.23.170.134:16283/?authSource=${authDatabase}`;
const client = new MongoClient(uri);

// Servers en Poorten
const LOCAL_PORT = 4000;
const PUBLIC_PORT = 5000;

const app = express();
app.use(cors());
app.use(bodyParser.json());

// ** Lokale Server voor interne endpoints **
const localServer = express();
localServer.use(cors());
localServer.use(bodyParser.json());

// Start de lokale server
localServer.listen(LOCAL_PORT, '127.0.0.1', async () => {
    console.log(`Lokale server draait op http://localhost:${LOCAL_PORT}`);
    try {
        await client.connect();
        await client.db(databaseName).command({ ping: 1 });
        console.log('Succesvol verbonden met MongoDB');
    } catch (err) {
        console.error('Kon geen verbinding maken met MongoDB:', err);
    }
});

// ** Publieke Server voor QR-code endpoint **
const publicServer = express();
publicServer.use(cors());
publicServer.use(bodyParser.json());

// Start de publieke server
publicServer.listen(PUBLIC_PORT, '0.0.0.0', () => {
    console.log(`Publieke server draait op http://0.0.0.0:${PUBLIC_PORT}`);
});

// ** Lokale Endpoints **
localServer.post('/save', async (req, res) => {
    const sessionId = Math.random().toString(36).substring(2, 15); // Genereer een random sessie-ID
    res.cookie('sessionId', sessionId); // Sla sessie-ID op in een cookie
    try {
        const { name, email, status } = req.body;
        const database = client.db(databaseName);
        const collection = database.collection(collectionName);

        const dataToSave = { 
            name, 
            email: email.trim().toLowerCase(), 
            status, 
            totalScore: 0,
            qrScanned: false,
        };
        

        await collection.insertOne(dataToSave);

        console.log('Data succesvol opgeslagen:', dataToSave);
        res.status(201).send('Data succesvol opgeslagen in MongoDB!');
    } catch (err) {
        console.error('Fout bij opslaan in MongoDB:', err);
        res.status(500).send('Er is een fout opgetreden bij het opslaan.');
    }
});

localServer.post('/add-score', async (req, res) => {
    try {
        const { email, name, totalScore } = req.body;
        const database = client.db(databaseName);
        const collection = database.collection(collectionName);

        if (!email || !name || typeof totalScore !== 'number') {
            res.status(400).send('Ongeldige gegevens: email, name en totalScore zijn vereist.');
            return;
        }

        const userExists = await collection.findOne({ email: email.trim().toLowerCase() });

        if (userExists) {
            await collection.updateOne(
                { email: email.trim().toLowerCase() },
                { $set: { name: name }, $inc: { totalScore: totalScore } }
            );
            console.log('Gebruiker gevonden. Score bijgewerkt.');
        } else {
            await collection.insertOne({
                name: name,
                email: email.trim().toLowerCase(),
                totalScore: totalScore
            });
            console.log('Nieuwe gebruiker toegevoegd.');
        }

        res.status(200).send('Score succesvol gekoppeld aan gebruiker!');
    } catch (err) {
        console.error('Fout bij koppelen van score:', err);
        res.status(500).send('Er is een fout opgetreden bij het koppelen van de score.');
    }
});

localServer.get('/top-scores', async (req, res) => {
    try {
        const database = client.db(databaseName);
        const collection = database.collection(collectionName);

        const topScores = await collection
            .find({}, { projection: { name: 1, totalScore: 1 } })
            .sort({ totalScore: -1 })
            .limit(10)
            .toArray();

        res.status(200).json(topScores);
    } catch (err) {
        console.error('Fout bij ophalen van scores:', err);
        res.status(500).send('Er is een fout opgetreden bij het ophalen van de scores.');
    }
});



