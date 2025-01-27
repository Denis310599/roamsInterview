from app.routes.routes import client_bp, user_bp

def register_routes(app):
  app.register_blueprint(client_bp)
  app.register_blueprint(user_bp)