from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        CONNECTION_STRING='188.166.83.105:27017',
        DATABASE='db'
    )

    @app.route('/hello')
    def hello():
        return 'The Doom has come to this world'

    from . import texts
    app.register_blueprint(texts.bp)

    return app