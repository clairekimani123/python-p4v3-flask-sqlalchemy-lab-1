#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)



@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    earthquake = Earthquake.query.filter_by(id=id).first()
    
    if earthquake:
        body = {
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }
        return make_response(jsonify(body), 200)
    else:
        body = {"message": f"Earthquake {id} not found."}
        return make_response(jsonify(body), 404)
    

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    body = {
        "count": len(earthquakes),
        "quakes": [
            {
                "id": eq.id,
                "location": eq.location,
                "magnitude": eq.magnitude,
                "year": eq.year
            } for eq in earthquakes
        ]
    }
    return make_response(jsonify(body), 200)  # ✅ 200 instead of 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
