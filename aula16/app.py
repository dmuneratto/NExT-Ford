
import os

from datetime import datetime
from unicodedata import category, name
from flask import Flask , abort, jsonify, render_template
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/aula16'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
api = Api(app)


db = SQLAlchemy(app)

# class Customer(db.Model, SerializerMixin):
#     
#     serialize_rules = ('-category','-orders.plate','-id', '-category_id')
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     address = db.Column(db.String(50), nullable=True)
#     phone =  db.Column(db.String(50), nullable=True)
#           
# 
# 
# category_id = db.Column(db.Integer, db.ForeignKey(
#         'category.id', ondelete="CASCADE"), nullable=False)
#     category = db.relationship(
#         'Category', back_populates='plate')
#     orders = db.relationship("PlateOrder", backref="plate")

#     def __repr__(self):
#         return '<Plate %r>' % self.name



class Plate(db.Model, SerializerMixin):
    #serialize_rules = ('-category.plate','-orders.plate',)
    serialize_rules = ('-category','-orders.plate','-id', '-category_id')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float(2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id', ondelete="CASCADE"), nullable=False)
    category = db.relationship(
        'Category', back_populates='plate')
    orders = db.relationship("PlateOrder", backref="plate")

    def __repr__(self):
        return '<Plate %r>' % self.name

class Category(db.Model, SerializerMixin):
    serialize_rules = ('-plate',)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    plate = db.relationship(
        'Plate',
        back_populates='category',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        passive_deletes=True,
        order_by='desc(Plate.name)'
    )
    
    def __repr__(self):
        return '<Category %r>' % self.name

class Orders(db.Model, SerializerMixin):
    serialize_rules = ('-plate.orders','-plate.plate.orders','-plate.order_id', '-plate.id')
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False, unique=True)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    plate = db.relationship("PlateOrder", backref="orders")

    def __repr__(self):
        return '<Order %r>' % self.name

class PlateOrder(db.Model, SerializerMixin):
    __tablename__ = 'plate_order'
    plate_id = db.Column(db.ForeignKey('plate.id'), primary_key=True)
    order_id = db.Column(db.ForeignKey('orders.id'), primary_key=True)
    amount = db.Column(db.Integer, nullable=False)




@app.before_first_request
def create_db():
    # Delete database file if it exists currently
    if os.path.exists("database.db"):
        os.remove("database.db")
    db.create_all()

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



@app.route('/')
def welcome():
    return "Bem vindo"

api.add_resource(PlateResource,"/Plates")
api.add_resource(PlateSearchResource,"/PlatesSearch")
api.add_resource(CategoryResource,"/Category")
api.add_resource(OrderResource,"/Orders")

@app.route('/Cadastra')
def registerplate():
    categories = Category.query.all() or abort(404, description="Resource not found")
    return render_template("newplate.html",categories=categories)


if __name__ == '__main__':
    app.run(debug=True)