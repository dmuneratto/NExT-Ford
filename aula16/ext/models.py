
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from aula16.ext.database import db


class Client(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50))
    phone = db.Column(db.String(14))
    orders = db.relationship('Orders', back_populates='client', lazy=True)


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
    client_id = db.Column(db.Integer, db.ForeignKey(
    'client.id', ondelete="CASCADE"), nullable=False)

    client = db.relationship(
    'Client', back_populates='orders')
    plate = db.relationship("PlateOrder", backref="orders")

    def __repr__(self):
        return '<Order %r>' % self.name

class PlateOrder(db.Model, SerializerMixin):
    __tablename__ = 'plate_order'
    plate_id = db.Column(db.ForeignKey('plate.id'), primary_key=True)
    order_id = db.Column(db.ForeignKey('orders.id'), primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
