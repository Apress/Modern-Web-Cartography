import os
from flask import Flask

def create_app(test_config=None):
    # Create and configure the application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # Load instance configuration, if any
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load test configuration
        app.config.from_mapping(test_config)

    # Check that the instance directory exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # A simple page that says Hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/map')
    def map():
        import folium
        m = folium.Map(location=[45.5236, -122.6750])
        return m._repr_html_()

    from prototypes import simple_maps
    app.register_blueprint(simple_maps.bp)

    from prototypes import advanced_maps
    app.register_blueprint(advanced_maps.bp)

    return app