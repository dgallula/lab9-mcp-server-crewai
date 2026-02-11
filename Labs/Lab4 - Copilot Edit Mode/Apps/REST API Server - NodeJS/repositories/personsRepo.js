const Person = require('../models/personModel');

// Get All
const getAllPersons = (filters) => {
  return Person.find(filters);
};

// Get By ID
const getPersonById = (id) => {
  return Person.findById(id);
};

// Create
const addPerson = (obj) => {
  const per = new Person(obj);
  return per.save();
};

// Update
const updatePerson = (id, obj) => {
  return Person.findByIdAndUpdate(id, obj);
};

// Delete
const deletePerson = (id) => {
  return Person.findByIdAndDelete(id);
};

module.exports = {
  getAllPersons,
  getPersonById,
  addPerson,
  updatePerson,
  deletePerson,
};
