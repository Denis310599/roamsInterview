from app.routes.routes import client_bp

def register_routes(app):
  app.register_blueprint(client_bp)