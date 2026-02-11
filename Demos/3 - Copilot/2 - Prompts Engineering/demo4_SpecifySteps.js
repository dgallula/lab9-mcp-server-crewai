// Create a js node js express server.

// 1. Import express
// 2. Create an express application
// 3. Define a port number
// 4. Set up a route for the root URL that sends "Hello World!" as a response
// 5. Start the server and listen on the defined port, logging a message to the console when it starts

const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
    res.send('Hello World!');
});

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`);
});