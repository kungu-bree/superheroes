from flask import Flask
from models import db, Power, Hero, HeroPower
from datetime import datetime
import random

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

with app.app_context():

    powers_data = [
        {"name": "super strength", "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ]

    for power_info in powers_data:
        power = Power(
            name=power_info["name"],
            description=power_info["description"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.session.add(power)

    heroes_data = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"}
    ]

    for hero_info in heroes_data:
        hero = Hero(
            name=hero_info["name"],
            super_name=hero_info["super_name"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(hero)

    strengths = ["Strong", "Weak", "Average"]
    heroes = Hero.query.all()

    for hero in heroes:
        for _ in range(random.randint(1, 3)):
            power = Power.query.get(random.choice(range(1, 5)))
            hero_power = HeroPower(
                hero_id=hero.id,
                power_id=power.id,
                strength=random.choice(strengths),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(hero_power)

    db.session.commit()

    print("🦸‍♀️ Done seeding!")