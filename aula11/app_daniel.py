from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'aaaaaa'


@app.route('/user')
def user():
    return 'meu usuario'

@app.route('/user/dashboard')
def dashboard():
    return 'dashboard'

if __name__ == '__main__':
    app.run()