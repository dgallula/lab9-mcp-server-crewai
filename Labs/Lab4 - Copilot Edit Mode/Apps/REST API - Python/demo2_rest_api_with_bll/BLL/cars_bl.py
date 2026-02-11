class CarsBL:
    def __init__(self):
        self.__cars = [
            {"id": 1, "model": "Mazda"},
            {"id": 2, "model": "BMW"}
        ]

    def get_all_cars(self):
        return self.__cars

    def get_car(self, id):
        arr = list(filter(lambda x: x["id"] == id, self.__cars))
        return arr[0]

    def add_car(self, obj):
        self.__cars.append(obj)

    def update_car(self, id, obj):
        for car in self.__cars:
            if car["id"] == id:
                car["model"] = obj["model"]
                break

    def delete_car(self, id):
        index = -1
        for i in range(len(self.__cars)):
            if self.__cars[i]["id"] == id:
                index = i
                break
        self.__cars.pop(index)
