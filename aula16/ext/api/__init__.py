from flask import Blueprint
from flask_restful import Api

from .resource import PlateResource, PlateSearchResource, OrderResource, CategoryResource

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")

api = Api(bp)


def init_app(app):
    api.add_resource(PlateResource,"/Plates")
    api.add_resource(PlateSearchResource,"/PlatesSearch")
    api.add_resource(CategoryResource,"/Category")
    api.add_resource(OrderResource,"/Orders")
    app.register_blueprint(bp)