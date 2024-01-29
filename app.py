

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource


from models import db, Hero, HeroPower, Power


app = Flask(_name_)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)




class Home(Resource):
def get(self):
   return 'Index for Hero,Hero_power,Power API'


api.add_resource(Home, '/')


class Heroes(Resource):
  def get(self):
     heroes_list = []
     for hero in Hero.query.all():
        hero_dict={
            "id": hero.id,
            "name":hero.name,
            "super_name":hero.super_name,
         }
        heroes_list.append(hero_dict)


     response = make_response(
         jsonify(heroes_list),
         200
      )
     response.headers["Content-Type"] = "application/json"
     return response
api.add_resource(Heroes, '/heroes')    


class HeroByID(Resource):
  def get(self,id):
     hero = Hero.query.filter_by(id=id).first()
     if hero:
        hero_dict={
           "id":hero.id,
           "name":hero.name,
           "super_name":hero.super_name,
           "created_at":hero.created_at,
           "updated_at":hero.updated_at
        }
        response = make_response(
             jsonify(hero_dict),
             200
         )
        response.headers["Content-Type"] = "application/json"
        return response
     else:
        response = make_response(
           jsonify({"error": "Power not found"}),
            404
         )
        response.headers["Content-Type"] = "application/json"
        return response




    
 
api.add_resource(HeroByID, '/heroes/<int:id>')


class Powers(Resource):
  def get(self):
   powers_list = []
   for power in Power.query.all():
       power_dict={
           "id": power.id,
           "name":power.name,
           "description":power.description,
       }
       powers_list.append(power_dict)


   response = make_response(
       jsonify(powers_list),
       200
   )
   response.headers["Content-Type"] = "application/json"
   return response
    
api.add_resource(Powers, '/powers')




class PowerByID(Resource):
  def get(self,id):
     power = Power.query.filter_by(id=id).first()  
     if power:
         power_dict = {
             "id": power.id,
             "name": power.name,
             "description": power.description,
         }
         response = make_response(
             jsonify(power_dict),
             200
         )
         response.headers["Content-Type"] = "application/json"
         return response
     else:
         response = make_response(
            jsonify({"error": "Power not found"}),
            404
         )
         response.headers["Content-Type"] = "application/json"
         return response
    
  def patch(self,id):
     try:
        power = Power.query.filter_by(id=id).first()
        if power:
           data = request.get_json()
           for attr in data:
              setattr(power, attr, data[attr])
           db.session.add(power)
           db.session.commit()
           return make_response(power.to_dict(),200)
        else:
           response={
              "error": "Power not found"
           }
           return jsonify(response), 404


     except Exception as e:
        response = {
            "errors": ["Validation errors"]
         }
        return jsonify(response), 422     
api.add_resource(PowerByID , '/powers/<int:id>') 


class HeroPowers(Resource):
  def post(self):
     try:
        data = request.get_json()
       
        strength = data.get("strength")
        power_id = data.get("power_id")
        hero_id = data.get("hero_id")
        new_record = HeroPower(
          strength= strength,
          power_id= power_id,
          hero_id= hero_id,
          )
        db.session.add(new_record)
        db.session.commit()
        record_dict = new_record.to_dict()
        response = make_response(
           jsonify(record_dict),
           200
         )
        return response
     except Exception as e:
        response={
           "errors": ["validation errors"]
        }
        return jsonify(response),500
    
api.add_resource(HeroPowers,'/hero_powers')






  




if _name_ == 'main':
   app.run(port=5555, debug=True)

