from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Power(db.Model):
    __tablename__ = 'power'
  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    
    @validates('description')
    def validate_description(self, key, value):
      if not value:
        raise ValueError(f"The description cannot be empty")
      return value

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    super_name = db.Column(db.String(50), nullable=False)   

    powers = db.relationship('Power', secondary='hero_power', backref='heroes')

    @validates('name', 'super_name')
    def validate_hero_name(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError(f"{key.capitalize()} cannot be empty.")
        return value

class HeroPower(db.Model):
    __tablename__ = 'hero_power'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(10), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)

    hero = db.relationship('Hero', backref='hero_powers')
    power = db.relationship('Power', backref='hero_powers')

    @validates('strength')
    def validate_strength(self, key, value):
        allowed_strengths = ["Strong", "Weak", "Average"]
        if value not in allowed_strengths:
            raise ValueError(f"Invalid strength value: {value}. Strength must be one of: {', '.join(allowed_strengths)}")
        return value
