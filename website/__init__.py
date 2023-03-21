from flask import Flask

def CreateApp():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "asdfasgasfsd"

    return app
    