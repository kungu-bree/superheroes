from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import  validates


db = SQLAlchemy()


class Hero(db.Model,SerializerMixin):
   tablename = 'heros'


   id = db.Column(db.Integer, primary_key=True)
  
   name=db.Column(db.String)
   super_name=db.Column(db.String)
   created_at=db.Column(db.DateTime())
   updated_at=db.Column(db.DateTime())


   hero_powers=db.relationship('HeroPower', backref='heros')


   def repr(self):
       return f'<Hero {self.super_name} for {self.name}>'         


class HeroPower(db.Model, SerializerMixin):
   tablename='hero_powers'


   id=db.Column(db.Integer, primary_key=True)
   strength=db.Column(db.String)
   created_at=db.Column(db.DateTime())
   updated_at=db.Column(db.DateTime())


   hero_id=db.Column(db.Integer, db.ForeignKey('hero.id'))
   power_id=db.Column(db.Integer, db.ForeignKey('power.id'))


   @validates('strength')
   def validate_strength(self, key, strength):
       if strength !='Strong' and strength !='Average' and strength !='Weak':
           raise ValueError('Strength must be one of the following values:Strong, Weak, Average')
       return strength


   def repr(self):
       return f'<HeroPower {self.strength}>'
  
  
class Power(db.Model, SerializerMixin):
   tablename='powers'


   id=db.Column(db.Integer, primary_key=True)
   name=db.Column(db.String)
   description=db.Column(db.String)
   created_at=db.Column(db.DateTime())
   updated_at=db.Column(db.DateTime())


   hero_powers=db.relationship('HeroPower', backref='powers')


   @validates('description')
   def validate_decription(self, key, description):
       if len(description) < 20:
           raise ValueError('Description must be at least 20 characters long')
       return description


   def repr(self):
       return f'<Power {self.description} for {self.name}>'

