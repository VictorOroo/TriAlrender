from api.models import Pizza, Restaurant, RestaurantPizza, db
from api.app import api
from flask_restful import Resource, reqparse
from flask import make_response, request, jsonify

class Index(Resource):
    def get(self):
        response_dict = {
            "index": "Welcome to pizza API",
        }
        return make_response(jsonify(response_dict), 200)

api.add_resource(Index, '/')

class Restaurants(Resource):
    def get(self):
        restaurants_dicts = [restaurant.to_dict() for restaurant in Restaurant.query.all()]
        return make_response(jsonify(restaurants_dicts), 200)

api.add_resource(Restaurants, '/restaurants')

class RestaurantByID(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            response_dict = {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address,
                "pizzas": [pizza.to_dict() for pizza in restaurant.pizzas]
            }
            return make_response(jsonify(response_dict), 200)
        else:
            response_dict = {"error": "Restaurant not found"}
            return make_response(jsonify(response_dict), 404)

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            for restaurant_pizza in restaurant.restaurant_pizzas:
                db.session.delete(restaurant_pizza)
            db.session.delete(restaurant)
            db.session.commit()
            return make_response('', 204)
        else:
            response_dict = {"error": "Restaurant not found"}
            return make_response(jsonify(response_dict), 404)

api.add_resource(RestaurantByID, '/restaurants/<int:id>')

class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        pizzas_dicts = [pizza.to_dict() for pizza in pizzas]
        return make_response(jsonify(pizzas_dicts), 200)

api.add_resource(Pizzas, '/pizzas')

class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()
        new_restaurant_pizza = RestaurantPizza(
            price=data.get('price'),
            pizza_id=data.get("pizza_id"),
            restaurant_id=data.get("restaurant_id"),
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        return make_response(new_restaurant_pizza.to_dict(), 201)

api.add_resource(RestaurantPizzas, '/restaurant_pizzas')
