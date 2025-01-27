from flask.cli import AppGroup
from app.models import db
from app.models.client import Client, User, Simulation

def register_cli_commands(app):
  db_cli = AppGroup('db')

  @db_cli.command('create')
  def create_db():
      """Create the database tables."""
      db.create_all()
      print("Database tables created.")


  app.cli.add_command(db_cli)

  @db_cli.command('populate')
  def populate_db():
    """Populates the tables with data"""
    clients = [
       Client(dni='43394140V', nombre='Rodrigo Perez', email='rodrigo@gmail.com', capital_solicitado=15000),
       Client(dni='32226717Z', nombre='John Doe', email='johndoe@gmail.com', capital_solicitado=5000), 
       Client(dni='15663962L', nombre='Shaun Murphy', email='shaunmurphy@gmail.com', capital_solicitado=35000) 
    ]

    users = [
       User(username='admin', passwd='1234'),
       User(username='user', passwd='1234'),
    ]

    db.session.bulk_save_objects(clients)
    db.session.bulk_save_objects(users)
    db.session.commit()
    print("Database populated successfully")



