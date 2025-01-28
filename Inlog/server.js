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
        const dataToSave = { name, email: email.trim().toLowerCase(), status, totalScore: 0, qrScanned: true};

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

// Endpoint om een score op te halen
app.get('/get-score', async (req, res) => {
    try {
        const email = req.query.email;
        if (!email) {
            res.status(400).send('Email is verplicht.');
            return;
        }

        await client.connect();
        const database = client.db(databaseName);
        const collection = database.collection(collectionName);

        const user = await collection.findOne({ email: email.trim().toLowerCase() });

        console.log(`Ophalen van gebruiker: ${email}`);
        if (user) {
            console.log(`Gevonden gebruiker: ${JSON.stringify(user)}`);
            res.status(200).json({ totalScore: user.totalScore || 0 });
        } else {
            console.log(`Gebruiker niet gevonden: ${email}`);
            res.status(404).send('Gebruiker niet gevonden.');
        }
    } catch (err) {
        console.error('Fout bij ophalen van score:', err);
        res.status(500).send('Er is een fout opgetreden bij het ophalen van de score.');
    } finally {
        await client.close();
    }
});

// Endpoint om de score te koppelen aan een ingelogde gebruiker
app.post('/add-score', async (req, res) => {
    try {
        await client.connect();
        const database = client.db(databaseName);
        const collection = database.collection(collectionName);

        const { email, name, totalScore } = req.body;

        if (!email || !name || typeof totalScore !== 'number') {
            console.error('Ongeldige gegevens ontvangen:', req.body);
            res.status(400).send('Ongeldige gegevens: email, name en totalScore zijn vereist.');
            return;
        }

        console.log(`Ontvangen payload: ${JSON.stringify(req.body)}`);

        // Controleer of gebruiker al bestaat
        const userExists = await collection.findOne({ email: email.trim().toLowerCase() });

        if (userExists) {
            // Verhoog de score als de gebruiker al bestaat
            const result = await collection.updateOne(
                { email: email.trim().toLowerCase() },
                {
                    $set: { name: name, email: email.trim().toLowerCase() },
                    $inc: { totalScore: totalScore }
                }
            );
            console.log('Gebruiker gevonden. Score bijgewerkt:', result);
        } else {
            // Voeg een nieuwe gebruiker toe als deze niet bestaat
            const result = await collection.insertOne({
                name: name,
                email: email.trim().toLowerCase(),
                totalScore: totalScore
            });
            console.log('Nieuwe gebruiker toegevoegd:', result);
        }

        res.status(200).send('Score succesvol gekoppeld aan gebruiker!');
    } catch (err) {
        console.error('Fout bij koppelen van score:', err);
        res.status(500).send('Er is een fout opgetreden bij het koppelen van de score.');
    } finally {
        await client.close();
    }
});

// Endpoint om de top 10 scores op te halen
app.get('/top-scores', async (req, res) => {
    try {
        await client.connect();
        const database = client.db(databaseName);
        const collection = database.collection(collectionName);

        const topScores = await collection
            .find({}, { projection: { name: 1, totalScore: 1 } }) // Haal alleen naam en score op
            .sort({ totalScore: -1 }) // Sorteer op totalScore (aflopend)
            .limit(10) // Beperk tot de top 10
            .toArray();

        res.status(200).json(topScores);
    } catch (err) {
        console.error('Fout bij ophalen van scores:', err);
        res.status(500).send('Er is een fout opgetreden bij het ophalen van de scores.');
    } finally {
        await client.close();
    }
});

// Endpoint om qrScanned op true te zetten en eventueel een score toe te voegen
app.post('/qr-scanned', async (req, res) => {
    try {
        const { email, scoreToAdd } = req.body;

        if (!email) {
            res.status(400).send('Email is verplicht.');
            return;
        }

        const scoreIncrement = typeof scoreToAdd === 'number' ? scoreToAdd : 0;

        console.log(`Zet qrScanned op true en voeg ${scoreIncrement} toe aan totalScore voor gebruiker met email: ${email}`);

        await client.connect();
        const database = client.db(databaseName);
        const collection = database.collection(collectionName);

        // Update qrScanned naar true en verhoog de score
        const result = await collection.updateOne(
            { email: email.trim().toLowerCase() },
            {
                $set: { qrScanned: true },
                $inc: { totalScore: scoreIncrement }
            }
        );

        if (result.matchedCount === 0) {
            console.log('Geen gebruiker gevonden met dat emailadres.');
            res.status(404).send('Gebruiker niet gevonden.');
            return;
        }

        console.log('qrScanned succesvol bijgewerkt en score toegevoegd.');
        res.status(200).send(`qrScanned succesvol bijgewerkt en ${scoreIncrement} toegevoegd aan totalScore!`);
    } catch (err) {
        console.error('Fout bij het bijwerken van qrScanned en totalScore:', err);
        res.status(500).send('Er is een fout opgetreden bij het bijwerken van qrScanned en totalScore.');
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
