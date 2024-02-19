from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

# Initialize SQLAlchemy
db = SQLAlchemy()

# Hero model
class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)
    
    powers = db.relationship('Power', secondary='hero_powers', backref='heroes_associated')

# Power model
# Power model
class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    heroes = db.relationship('Hero', secondary='hero_powers', backref='heroes_associated')

    # Validation for description length
    @validates('description')
    def validate_description(self, key, description):
        if len(description.strip()) < 20:
            raise ValueError('Description must be at least 20 characters long')
        return description



# HeroPower model
class HeroPower(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    strength = db.Column(db.String(255), nullable=False)

    # Validation for strength values
    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength not in valid_strengths:
            raise ValueError('Strength must be one of: Strong, Weak, Average')
        return strength

    # Relationships
    hero = db.relationship('Hero', backref='hero_powers')
    power = db.relationship('Power', backref='hero_powers')
