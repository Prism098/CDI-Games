const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const { MongoClient, ObjectId } = require('mongodb');

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

// Endpoint om een nieuwe gebruiker op te slaan
app.post('/save', async (req, res) => {
    try {
        const database = client.db(databaseName);
        const collection = database.collection(collectionName);

        const { name, email, status } = req.body;
        const dataToSave = { name, email, status, totalScore: 0, createdAt: new Date() };

        await collection.insertOne(dataToSave);

        console.log('Data succesvol opgeslagen:', dataToSave);
        res.status(201).send('Data succesvol opgeslagen in MongoDB!');
    } catch (err) {
        console.error('Fout bij opslaan in MongoDB:', err);
        res.status(500).send('Er is een fout opgetreden bij het opslaan.');
    }
});

// Endpoint om de laatst aangemaakte gebruiker op te halen
app.get('/last-user', async (req, res) => {
    try {
        const database = client.db(databaseName);
        const collection = database.collection(collectionName);

        const lastUser = await collection.find({}).sort({ createdAt: -1 }).limit(1).toArray();

        if (lastUser.length === 0) {
            return res.status(404).send('Geen gebruikers gevonden.');
        }

        res.status(200).json(lastUser[0]);
    } catch (err) {
        console.error('Fout bij ophalen van laatste gebruiker:', err);
        res.status(500).send('Er is een fout opgetreden bij het ophalen van de laatste gebruiker.');
    }
});

// Endpoint om score toe te voegen aan de laatst aangemaakte gebruiker
app.post('/add-score', async (req, res) => {
    const { totalScore } = req.body;

    if (totalScore == null || totalScore <= 0) {
        return res.status(400).send('Een geldige score groter dan 0 is verplicht.');
    }

    try {
        const database = client.db(databaseName);
        const collection = database.collection(collectionName);

        const lastUser = await collection.find({}).sort({ createdAt: -1 }).limit(1).toArray();

        console.log('Laatst gevonden gebruiker:', lastUser);

        if (lastUser.length === 0) {
            return res.status(404).send('Geen gebruikers gevonden.');
        }

        const userId = new ObjectId(lastUser[0]._id);
        const updatedUser = await collection.updateOne(
            { _id: userId },
            { $inc: { totalScore: totalScore } }
        );

        console.log('Update resultaat:', updatedUser);

        if (updatedUser.matchedCount === 0) {
            return res.status(404).send('Gebruiker niet gevonden.');
        }

        res.status(200).send('Score succesvol toegevoegd aan de laatste gebruiker!');
    } catch (err) {
        console.error('Fout bij toevoegen van score:', err);
        res.status(500).send('Er is een fout opgetreden bij het toevoegen van de score.');
    }
});

// Endpoint om data naar een tekstbestand te exporteren
app.get('/export-data', async (req, res) => {
    try {
        const database = client.db(databaseName);
        const collection = database.collection(collectionName);

        const allData = await collection.find({}).toArray();

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
    }
});

// Nieuw endpoint: Haal de top 10 scores op
app.get('/top-scores', async (req, res) => {
    try {
        const database = client.db(databaseName);
        const collection = database.collection(collectionName);

        // Vind gebruikers, sorteer op totalScore (hoog naar laag), limiet 10
        const topScores = await collection.find({})
            .sort({ totalScore: -1 }) // Sorteer op score aflopend
            .limit(10) // Top 10
            .toArray();

        res.status(200).json(topScores);
    } catch (err) {
        console.error('Fout bij ophalen van top scores:', err);
        res.status(500).send('Er is een fout opgetreden bij het ophalen van de top scores.');
    }
});
