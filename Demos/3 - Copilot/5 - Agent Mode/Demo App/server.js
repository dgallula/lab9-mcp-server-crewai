const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

const db = new sqlite3.Database('./recipes.db');

// Get random recipe by mood
app.get('/api/recipe/:mood', (req, res) => {
  const mood = req.params.mood;
  
  const query = 'SELECT * FROM recipes WHERE mood = ? ORDER BY RANDOM() LIMIT 1';
  
  db.get(query, [mood], (err, row) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    if (!row) {
      res.status(404).json({ error: 'No recipe found for this mood' });
      return;
    }
    res.json(row);
  });
});

// Get all available moods
app.get('/api/moods', (req, res) => {
  const query = 'SELECT DISTINCT mood FROM recipes';
  
  db.all(query, [], (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json(rows.map(row => row.mood));
  });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
