from flask.cli import AppGroup
from app.models import db, client

def register_cli_commands(app):
  db_cli = AppGroup('db')

  @db_cli.command('create')
  def create_db():
      """Create the database tables."""
      db.create_all()
      print("Database tables created.")


  app.cli.add_command(db_cli)