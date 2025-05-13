# Main application factory
from flask import Flask
from flask_cors import CORS

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Enable CORS to support cross-origin requests
    CORS(app)
    
    # Load configuration
    from config.settings import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    
    # Initialize database
    from models.db import init_app as init_db
    init_db(app)
    
    # Register routes
    from routes import init_app as init_routes
    init_routes(app)
    
    return app


# For direct execution
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)