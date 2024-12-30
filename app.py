from flask import Flask, request, session, jsonify
from flask_babel import Babel
from views.main import main_bp
import config
import os

babel = Babel()

def get_locale():
    """Get the locale for the current request."""
    if 'lang' in session:
        return session['lang']
    return request.accept_languages.best_match(config.SUPPORTED_LANGUAGES)

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config)
    
    # Initialize Babel
    babel.init_app(app, locale_selector=get_locale)
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    
    @app.route('/set_language/<language>', methods=['POST'])
    def set_language(language):
        if language in app.config['SUPPORTED_LANGUAGES']:
            session['lang'] = language
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Invalid language'})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5002, debug=True)
