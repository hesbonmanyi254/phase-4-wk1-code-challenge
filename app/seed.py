from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import Hero, Power, HeroPower

# Create the Flask application instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

# Use the application context
with app.app_context():
    # Create Heroes
    heroes_data = [
        {'name': 'Superman', 'super_name': 'Clark Kent'},
        {'name': 'Batman', 'super_name': 'Bruce Wayne'},
        {'name': 'Wonder Woman', 'super_name': 'Diana Prince'}
    ]

    heroes = []
    for hero_data in heroes_data:
        hero = Hero(**hero_data)
        heroes.append(hero)

    db.session.add_all(heroes)
    db.session.commit()

    # Create Powers
    powers_data = [
        {'name': 'Flight', 'description': 'Ability to fly and soar high in the sky'},
        {'name': 'Super Strength', 'description': 'Ability to exhibit superhuman strength and lift heavy objects'},
        {'name': 'Invisibility', 'description': 'Ability to become invisible and move unseen'}
    ]


    powers = []
    for power_data in powers_data:
        power = Power(**power_data)
        powers.append(power)

    db.session.add_all(powers)
    db.session.commit()

    # Create HeroPowers
    hero_powers_data = [
        {'hero_id': 1, 'power_id': 1, 'strength': 'Strong'},
        {'hero_id': 1, 'power_id': 2, 'strength': 'Strong'},
        {'hero_id': 2, 'power_id': 2, 'strength': 'Average'},
        {'hero_id': 3, 'power_id': 1, 'strength': 'Average'},
        {'hero_id': 3, 'power_id': 3, 'strength': 'Weak'}
    ]

    hero_powers = []
    for hero_power_data in hero_powers_data:
        hero_power = HeroPower(**hero_power_data)
        hero_powers.append(hero_power)

    db.session.add_all(hero_powers)
    db.session.commit()

    print('Database seeded successfully!')
