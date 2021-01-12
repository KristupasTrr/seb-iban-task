import flask
from api.route.iban import iban_api
from main.home import home_page

def create_app():
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True

    app.register_blueprint(iban_api, url_prefix='/api/iban')
    app.register_blueprint(home_page, url_prefix='/')

    return app

if __name__ == "__main__":
    app = create_app()

    app.run()