
from flask import jsonify, Blueprint
from flask_restful import Resource, reqparse, abort
from aula16.ext.models import Category, Plate, Orders
from aula16.ext.database import db


class PlateResource(Resource):
    def get(self):
        plates = Plate.query.all() or abort(404, description="Resource not found")
        return jsonify({"Plates": [plate.to_dict(rules=('-category_id','-orders')) for plate in plates]}
             
        )

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=ascii,help='recurso não enviado, prfv mande um nome')
        parser.add_argument('price', type=float)
        parser.add_argument('category_id', type=int)

        args = parser.parse_args()

        plate = Plate(**args)
        db.session.add(plate)
        db.session.commit()

        return jsonify({"success": True, "response": "Plate added"})

    def put(self):
        pass

    def delete(self):
        pass


class PlateSearchResource(Resource):
    def get(self, plate_id):
        plate = Plate.query.filter_by(id=plate_id).first() or abort(404, description="Resource not found")
        return jsonify(plate.to_dict()) 
             
        
class CategoryResource(Resource):
    def get(self):
        categories = Category.query.all() or abort(404, description="Resource not found")
        return jsonify(
            {"Categories": [category.to_dict() for category in categories]})
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=ascii,help='recurso não enviado, prfv mande um nome')
        args = parser.parse_args()

        category = Category(**args)
        db.session.add(category)
        db.session.commit()

        return jsonify({"success": True, "response": "Category added"})
                 

class OrderResource(Resource):
    def get(self):
        orders = Orders.query.all() or abort(404, description="Resource not found")
        return jsonify(
            {"Order": [order.to_dict() for order in orders]}
        )
