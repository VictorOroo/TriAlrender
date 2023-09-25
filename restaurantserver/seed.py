
from faker import Faker
from api.models import db, Restaurant, Pizza, RestaurantPizza
from api.app import app
import random

random.seed(42)

fake = Faker()

with app.app_context():
    Restaurant.query.delete()
    Pizza.query.delete()
    RestaurantPizza.query.delete()

    
    restaurants = [
        Restaurant(name=fake.company(), address=fake.address()) for _ in range(50)
    ]
    db.session.add_all(restaurants)
    db.session.commit()

    
    pizzas = [
        Pizza(name=fake.name(), ingredients=', '.join([' '.join(fake.words(3)) for _ in range(7)])) for _ in range(50)
    ]
    db.session.add_all(pizzas)
    db.session.commit()

    
    restaurant_pizzas = []
    for restaurant in Restaurant.query.all():
        pizza_count = random.randint(1, 10)
        for _ in range(pizza_count):
            new_restaurant_pizza = RestaurantPizza(
                pizza_id=random.choice(pizzas).id,
                restaurant_id=restaurant.id,
                price=random.randint(1, 30)
            )
            restaurant_pizzas.append(new_restaurant_pizza)

    db.session.add_all(restaurant_pizzas)
    db.session.commit()
