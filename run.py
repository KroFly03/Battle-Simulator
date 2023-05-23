from flask import Flask
from blueprints import index, prep, fight


app = Flask(__name__)

app.register_blueprint(index)
app.register_blueprint(prep)
app.register_blueprint(fight)

if __name__ == '__main__':
    app.run()
