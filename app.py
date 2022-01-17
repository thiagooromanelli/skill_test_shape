from flask import Flask
from flask_migrate import Migrate
from config.config import Config
from api.routes.routes import api
from database.database import db


def create_app():
    app = Flask(__name__)

    app.config['SWAGGER'] = {
        'title': 'Application Swagger',
    }
    app.config.from_object(Config)
    app.register_blueprint(api, url_prefix='/api')

    db.init_app(app)
    migrate = Migrate(app, db)

    return app


if __name__ == '__main__':
    my_app = create_app()
    my_app.run(host='0.0.0.0', port=5000, debug=True)
