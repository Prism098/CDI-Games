const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
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

app.use(cors());
app.use(bodyParser.json());

// ================== 1) CONNECT ONCE AT SERVER START  ==================
app.listen(PORT, async () => {
  console.log(`Server running on http://localhost:${PORT}`);
  try {
    await client.connect();  // Connect once
    await client.db(databaseName).command({ ping: 1 });
    console.log('Succesvol verbonden met MongoDB');
  } catch (err) {
    console.error('Kon geen verbinding maken met MongoDB:', err);
  }
});



// Endpoint om data op te slaan in MongoDB
app.post('/save', async (req, res) => {
  try {
    // NO: await client.connect();
    const db = client.db(databaseName);
    const collection = db.collection(collectionName);

    const { name, email, status } = req.body;
    const currentDateTime = new Date();

    const dataToSave = { 
      name, 
      email: email.trim().toLowerCase(), 
      status, 
      totalScore: 0, 
      qrScanned: false,
      createdAt: currentDateTime
    };

    const result = await collection.insertOne(dataToSave);
    console.log('Data succesvol opgeslagen:', dataToSave);
    res.status(201).json({ 
      message: 'Data succesvol opgeslagen in MongoDB!', 
      id: result.insertedId  
    });
  } catch (err) {
    console.error('Fout bij opslaan in MongoDB:', err);
    res.status(500).send('Er is een fout opgetreden bij het opslaan.');
  }
  // DO NOT close client here
});

// Endpoint om een score op te halen
app.get('/get-score', async (req, res) => {
  try {
    const email = req.query.email;
    if (!email) {
      return res.status(400).send('Email is verplicht.');
    }

    const db = client.db(databaseName);
    const collection = db.collection(collectionName);

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
  }
});

// Endpoint om de score te koppelen aan een ingelogde gebruiker
app.post('/add-score', async (req, res) => {
  try {
    const db = client.db(databaseName);
    const collection = db.collection(collectionName);

    const { email, name, totalScore } = req.body;
    if (!email || !name || typeof totalScore !== 'number') {
      console.error('Ongeldige gegevens ontvangen:', req.body);
      return res.status(400).send('Ongeldige gegevens: email, name en totalScore zijn vereist.');
    }

    console.log(`Ontvangen payload: ${JSON.stringify(req.body)}`);

    const userExists = await collection.findOne({ email: email.trim().toLowerCase() });

    if (userExists) {
      const result = await collection.updateOne(
        { email: email.trim().toLowerCase() },
        {
          $set: { name: name, email: email.trim().toLowerCase() },
          $inc: { totalScore: totalScore }
        }
      );
      console.log('Gebruiker gevonden. Score bijgewerkt:', result);
    } else {
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
  }
});

// Endpoint om de top 10 scores op te halen
app.get('/top-scores', async (req, res) => {
  try {
    const db = client.db(databaseName);
    const collection = db.collection(collectionName);

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

// GET /recent-scores
app.get('/recent-scores', async (req, res) => {
    try {
      // Use the existing open client connection (no connect/close per request)
      const db = client.db(databaseName);
      const collection = db.collection(collectionName);
  
      // Filter out docs with totalScore = 0
      const recentScores = await collection
        .find({ totalScore: { $gt: 0 } }, { projection: { name: 1, totalScore: 1, createdAt: 1 } })
        .sort({ createdAt: -1 })
        .limit(10)
        .toArray();
  
      res.status(200).json(recentScores);
    } catch (err) {
      console.error('Fout bij ophalen van recente scores:', err);
      res.status(500).send('Er is een fout opgetreden bij het ophalen van de recente scores.');
    }
  });

// Endpoint om qrScanned op true te zetten en eventueel een score toe te voegen
app.post('/qr-scanned', async (req, res) => {
  try {
    const { email, scoreToAdd } = req.body;
    if (!email) {
      return res.status(400).send('Email is verplicht.');
    }

    const db = client.db(databaseName);
    const collection = db.collection(collectionName);

    const scoreIncrement = typeof scoreToAdd === 'number' ? scoreToAdd : 0;
    console.log(`Zet qrScanned op true en voeg ${scoreIncrement} toe aan totalScore: ${email}`);

    const result = await collection.updateOne(
      { email: email.trim().toLowerCase() },
      {
        $set: { qrScanned: true },
        $inc: { totalScore: scoreIncrement }
      }
    );

    if (result.matchedCount === 0) {
      console.log('Geen gebruiker gevonden met dat emailadres.');
      return res.status(404).send('Gebruiker niet gevonden.');
    }

    console.log('qrScanned succesvol bijgewerkt en score toegevoegd.');
    res.status(200).send(`qrScanned en +${scoreIncrement} toegevoegd aan totalScore!`);
  } catch (err) {
    console.error('Fout bij qrScanned:', err);
    res.status(500).send('Er is een fout opgetreden bij qrScanned.');
  }
});

// Nieuw: Endpoint om data naar een tekstbestand te exporteren
app.get('/export-data', async (req, res) => {
  try {
    const db = client.db(databaseName);
    const collection = db.collection(collectionName);

    const allData = await collection.find({}).toArray();
    const formatted = allData.map(doc => JSON.stringify(doc, null, 2)).join('\n\n');

    const filePath = 'exported_data.txt';
    fs.writeFileSync(filePath, formatted);

    console.log(`Data succesvol geëxporteerd naar ${filePath}`);
    res.status(200).send(`Data succesvol geëxporteerd naar ${filePath}`);
  } catch (err) {
    console.error('Fout bij exporteren van data:', err);
    res.status(500).send('Er is een fout bij export.');
  }
});
