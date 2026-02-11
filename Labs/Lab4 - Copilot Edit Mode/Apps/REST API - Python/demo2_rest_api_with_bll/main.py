from flask import Flask
from flask import jsonify
from flask import request

from BLL.cars_bl import *

app = Flask(__name__)

cars_bl = CarsBL()


@app.route("/cars", methods=["GET"])
def get_all_cars():
    return jsonify(cars_bl.get_all_cars())


@app.route("/cars/<int:id>", methods=["GET"])
def get_car(id):
    return jsonify(cars_bl.get_car(id))


@app.route("/cars", methods=["POST"])
def create_car():
    cars_bl.add_car(request.json)
    return jsonify("Created")


@app.route("/cars/<int:id>", methods=["PUT"])
def update_car(id):
    cars_bl.update_car(id, request.json)
    return jsonify("Updated")


@app.route("/cars/<int:id>", methods=["DELETE"])
def delete_car(id):
    cars_bl.delete_car(id)
    return jsonify("Deleted")


app.run()
