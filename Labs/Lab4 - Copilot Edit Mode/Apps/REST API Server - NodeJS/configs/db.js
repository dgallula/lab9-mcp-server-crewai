const mongoose = require('mongoose');

const connectDB = () => {
  // mongoose.connect('mongodb://127.0.0.1:27017/personsDB')
  mongoose
    .connect('mongodb://localhost:27017/personsDB')
    .then(() => console.log('connected to personsDB'))
    .catch(console.log);
};

module.exports = connectDB;
