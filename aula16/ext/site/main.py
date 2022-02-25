from flask import Blueprint, render_template, abort
from aula16.ext.models import Category

bp = Blueprint("site", __name__, template_folder="templates")

@bp.route('/')
def welcome():
    return "Bem vindo"

@bp.route('/Cadastra')
def registerplate():
    categories = Category.query.all() or abort(404, description="Resource not found")
    return render_template("newplate.html",categories=categories)