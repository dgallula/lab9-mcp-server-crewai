// write a function that send a HTTP GET request to a server that retuerns 
// an array of User objects. 
// the server "https://jsonplaceholder.typicode.com/users"

const https = require('https');
const fetch = require('node-fetch');
const axios = require('axios');

function fetchUsers() {
    return fetch('https://jsonplaceholder.typicode.com/users')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            throw new Error("HTTP request failed: " + error.message);
        });
}

function fetchUsersWithAxios() {
    return axios.get('https://jsonplaceholder.typicode.com/users')
        .then(response => response.data)
        .catch(error => {
            throw new Error("HTTP request failed: " + error.message);
        });
}