const express = require('express');
const cors = require('cors');
const connectDB = require('./configs/db');

const personsRouter = require('./routers/personsRouter');

const app = express();
const PORT = 3000;

connectDB();

app.use(cors());

app.use(express.json());

app.use('/persons', personsRouter);

app.listen(PORT, () => {
  // Entry Point (Base URL): http://localhost:3000
  console.log(`app is listening at http://localhost:${PORT}`);
});
