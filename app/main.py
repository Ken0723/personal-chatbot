from flask import Flask
from flask_cors import CORS
from app.routes.api_routes import api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": ["https://ken-yeung.me", "http://localhost:3000"]}})

    # Allowed request's method config
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST')
        return response
    
    # Blue print register
    app.register_blueprint(api, url_prefix='/api')

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8086)
