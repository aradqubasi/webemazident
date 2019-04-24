from flask import Flask, render_template, redirect, url_for
import os

def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        CONNECTION_STRING=os.environ.get('CONNECTION_STRING'),
        DATABASE=os.environ.get('DATABASE'),
        GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY'),
        RAPID_API_KEY=os.environ.get('RAPID_API_KEY'),
        GEMOTION_AUTH_TOKEN=os.environ.get('GEMOTION_AUTH_TOKEN')
    )

    @app.route('/')
    def hello():
        return redirect(url_for('texts.index'))

    from . import texts
    app.register_blueprint(texts.bp)

    from . import text
    app.register_blueprint(text.bp)

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html', error=error), 500

    return app