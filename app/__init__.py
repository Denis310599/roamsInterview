from flask import Flask
from app.routes import register_routes
from .logging_config import setup_logging
from flask_jwt_extended import (JWTManager)
import app.config as config

def create_app():
  #Init App
  app = Flask(__name__)

  #Sets up config
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
  app.config["JWT_SECRET_KEY"] = config.JWT_SECRET
  app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.JWT_EXPIRATION_TIME
  

  jwt = JWTManager(app)
  
  # Set up logging
  logger = setup_logging()
  app.logger = logger  # Attach the logger to the app


  
  #Initialize DB
  from app.models import db
  db.init_app(app)


  #register CLI commands
  from app.cli import register_cli_commands
  register_cli_commands(app)

  #Register routes
  register_routes(app)
  

  return app