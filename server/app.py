#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        all_plants=Plant.query.all()
        return make_response(jsonify(all_plants))
    

    def post(self):
        data = request.get_json()
        name = Plant(data['name'])
        price = Plant(data['price'])
        image = Plant(data['image'])

        new_plant =Plant(name,image,price)
        db.session.add(new_plant)
        db.session.commit()

        return new_plant.to_dict()
    
api.add_resource(Plants, '/plants','/add_plant')

class PlantByID(Resource):
    def plant_by_id(self,id):
        plant_by_id = Plant.query.filter_by(id=id).first()

        return plant_by_id.to_dict()
    
    def delete(self,id):
        del_plant = Plant.query.filter_by(id=id).first()
        db.session.delete(del_plant)
        db.session.commit()

        return  f'plant id {id} deleted successifuly'

api.add_resource(PlantByID, '/plants/<int:plant_id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
