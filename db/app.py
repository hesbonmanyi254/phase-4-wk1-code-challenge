from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models import db, Power, Hero, HeroPower

app = Flask(__name__)

# Configure the database URI and disable tracking modifications
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes_powers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking modifications to avoid warning

CORS(app) # Enable CORS fro all routes
migrate = Migrate(app, db) # Initialize hte Flask SQLAlchemy and Flask-Migrate

db.init_app(app)

# A custom exception class for validation errors
class ValidationError(Exception):
  def __init__(self, errors):
    self.errors = errors        
        
# A custom error handler to return validation errors in a consistent format
@app.errorhandler(ValidationError)
def handle_validation_error(error):
    response = jsonify({"errors": error.errors})
    response.status_code = 400
    return response        

# GET a list of all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heroes]
    return jsonify(heroes_data)

# Get list of heroes by ID
@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [
                {"id": power.id, "name": power.name, "description": power.description}
                for power in hero.powers
            ]
        }
        return jsonify(hero_data)
    else:
        return jsonify({"error": "Hero not found"}), 404


# GET a list of all powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [{"id": power.id, "name": power.name, "description": power.description} for power in powers]
    return jsonify(powers_data)


# GET info of a power by ID or update the description using PATCH method
@app.route('/powers/<int:power_id>', methods=['GET', 'PATCH'])
def get_or_update_power(power_id):
    # Check if the request method is GET
    if request.method == 'GET':
        # Retrieve the Power record with the given ID
        power = Power.query.get(power_id)
        if power:
            # Return JSON data for the Power record
            power_data = {"id": power.id, "name": power.name, "description": power.description}
            return jsonify(power_data)
        else:
            # Return an error message if the Power record is not found
            return jsonify({"error": "Power not found"}), 404
    
    # Check if the request method is PATCH
    elif request.method == 'PATCH':
        # Retrieve the Power record with the given ID
        power = Power.query.get(power_id)
        if not power:
            # Return an error message if the Power record is not found
            return jsonify({"error": "Power not found"}), 404

        # Retrieve JSON data from the request
        data = request.get_json()
        new_description = data.get('description')

        # Check if the new description is provided
        if new_description:
            # Update the description of the Power record
            power.description = new_description
            try:
                # Commit the changes to the database
                db.session.commit()
                return jsonify({"id": power.id, "name": power.name, "description": power.description})
            except IntegrityError:
                # Rollback changes and return validation errors if there are integrity errors
                db.session.rollback()
                return jsonify({"errors": ["Validation errors"]}), 400
        else:
            # Return an error message if the new description is empty
            return jsonify({"errors": ["Description cannot be empty"]}), 400


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    validation_errors = []

    if not power:
      validation_errors.append(f"Power cannot be empty.")

    if not hero:
      validation_errors.append(f"Hero cannot be empty.")
        
    if not strength:
      validation_errors.append(f"Strength cannot be empty.")

    elif strength not in ["Strong", "Weak", "Average"]:
        validation_errors.append(f"Invalid strength value: {strength}. Strength must be one of: Strong, Weak, Average.(Include CAPS)")

    if validation_errors:
        raise ValidationError(validation_errors)

    hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
    db.session.add(hero_power)

    try:
        db.session.commit()
        return jsonify({
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [{"id": p.id, "name": p.name, "description": p.description} for p in hero.powers]
        })
    except IntegrityError:
        db.session.rollback()
        raise ValidationError(["Validation errors"])
      
      
if __name__ == '__main__':    
    app.run(debug=True)
