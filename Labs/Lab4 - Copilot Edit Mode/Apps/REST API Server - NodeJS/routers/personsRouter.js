const express = require('express');
const personsService = require('../services/personsService');

const router = express.Router();

// Entry Point: http://localhost:3000/persons

// Get all Persons
router.get('/', async (req, res) => {
  try {
    const filters = req.query;
    const persons = await personsService.getAllPersons(filters);
    res.send(persons);
  } catch (error) {
    res.status(500).send(error);
  }
});

// Get all cities
router.get('/cities', async (req, res) => {
  try {
    const cities = await personsService.getAllCities();
    res.send(cities);
  } catch (error) {
    res.status(500).send(error);
  }
});

// Get Person by ID
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const person = await personsService.getPersonById(id);
    res.send(person);
  } catch (error) {
    res.status(500).send(error);
  }
});

// Add a new Person
router.post('/', async (req, res) => {
  try {
    const perData = req.body;
    const newPer = await personsService.addPerson(perData);
    res.status(201).send(`The new ID: ${newPer._id}`);
  } catch (error) {
    res.status(400).send(error);
  }
});

// Update a Person
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const perData = req.body;
    const result = await personsService.updatePerson(id, perData);
    res.send(result);
  } catch (error) {
    res.status(500).send(error);
  }
});

// Delete a Person
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const deletedPer = await personsService.deletePerson(id);
    res.send(deletedPer);
  } catch (error) {
    res.status(500).send(error);
  }
});

module.exports = router;
