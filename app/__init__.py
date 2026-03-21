# app/__init__.py
from flask import Flask
import os

def create_app():
    app = Flask(__name__) 
    
    # Build Css Automaticli
    
    
    # Routes handel all Blueprints
    from .routes import main
    
    app.register_blueprint(main)
    # need to be reorganized
    from .api import api

    app.register_blueprint(api)

    return app
