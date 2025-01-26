from flask import Flask
from app.routes import register_routes
from .logging_config import setup_logging

def create_app():
  #Init App
  app = Flask(__name__)
  
  # Set up logging
  logger = setup_logging()
  app.logger = logger  # Attach the logger to the app


  #Sets up config
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

  #Initialize DB
  from app.models import db
  db.init_app(app)


  #register CLI commands
  from app.cli import register_cli_commands
  register_cli_commands(app)

  #Register routes
  register_routes(app)
  

  return app