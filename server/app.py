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
        plants = Plant.query.all()  # Fetch all plants
        all_plants = [plant.to_dict() for plant in plants]  # Convert each plant to a dictionary
        return make_response(jsonify(all_plants), 200)  # Return serialized data with a 200 status code

    def post(self):
        data = request.get_json()

        # Create a new Plant object with the correct arguments
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )

        db.session.add(new_plant)  # Add the new plant to the session
        db.session.commit()  # Commit the session to persist the data

        # Return the serialized new plant object with a 201 status code
        return make_response(jsonify(new_plant.to_dict()), 201)
    
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, plant_id):
        plant_by_id = Plant.query.filter_by(id=plant_id).first()
        if plant_by_id:
            return make_response(jsonify(plant_by_id.to_dict()), 200)
        else:
            return make_response(jsonify({"error": "Plant not found"}), 404)

    def delete(self, plant_id):
        del_plant = Plant.query.filter_by(id=plant_id).first()
        if del_plant:
            db.session.delete(del_plant)
            db.session.commit()
            return make_response(f'Plant with ID {plant_id} deleted successfully', 200)
        else:
            return make_response(f'Plant with ID {plant_id} not found', 404)
    

api.add_resource(PlantByID, '/plants/<int:plant_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
