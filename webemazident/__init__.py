from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        CONNECTION_STRING='mongodb://DbAdmin:1app1Mongo@165.227.154.157:27017',
        DATABASE='dev-1'
    )

    @app.route('/hello')
    def hello():
        return 'The Doom has come to this world'

    from . import texts
    app.register_blueprint(texts.bp)

    from . import text
    app.register_blueprint(text.bp)

    return app