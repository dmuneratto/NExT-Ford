from flask import Flask 

from aula16.ext import database
from aula16.ext import config
from aula16.ext import site
from aula16.ext import api


app = Flask(__name__)
config.init_app(app)
database.init_app(app)
site.init_app(app)
api.init_app(app)




""" @app.before_first_request
def create_db():
    # Delete database file if it exists currently
    if os.path.exists("database.db"):
        os.remove("database.db")
    db.create_all() """


""" if __name__ == '__main__':
    app.run(debug=True) """