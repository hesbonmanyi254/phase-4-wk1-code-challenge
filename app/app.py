#!/usr/bin/env python3

# Import necessary modules
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from flask_migrate import Migrate
from marshmallow.exceptions import ValidationError
from flask_cors import CORS

# Import models from models.py
from models import db, Hero, Power, HeroPower

# Create Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
migrate = Migrate(app, db)
db.init_app(app)

# Enable CORS for all routes
CORS(app)

# Home route
@app.route('/')
def home():
    return ''

# Route to get all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    result = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(result)

# Route to get a specific hero by id
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    powers = [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
    result = {'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': powers}
    return jsonify(result)

# Route to get all powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    result = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(result)

# Route to get a specific power by id
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    result = {'id': power.id, 'name': power.name, 'description': power.description}
    return jsonify(result)

# Route to update a power's description
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    data = request.get_json()
    try:
        power.description = data['description']
        db.session.commit()
        return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
    except KeyError:
        return jsonify({'errors': ['description is required']}), 400
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400

# Route to create a hero power association
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    try:
        hero_id = data['hero_id']
        power_id = data['power_id']
        strength = data['strength']
    except KeyError:
        return jsonify({'errors': ['hero_id, power_id, and strength are required']}), 400
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)
    if not hero or not power:
        return jsonify({'error': 'Hero or Power not found'}), 404
    try:
        hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
        db.session.add(hero_power)
        db.session.commit()
        return jsonify(get_hero(hero_id))
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400

# Run the app if this file is executed
if __name__ == '__main__':
    app.run(port=5555)
