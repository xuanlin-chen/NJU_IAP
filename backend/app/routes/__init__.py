# Routes package initialization
from flask import Response, jsonify

# Common API response format
def api_response(data=None, message="success", code=200, errors=None) -> Response:
    response = {
        "code": code,
        "message": message,
        "data": data
    }
    if errors:
        response["errors"] = errors
    return jsonify(response)

# Include all route modules
def init_app(app):
    """Initialize all routes with the app"""
    from .api_routes import api_bp
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')