from datetime import timedelta
import os

JWT_EXPIRATION_TIME = timedelta(hours=1)
JWT_SECRET = os.environ['JWT_SECRET_KEY']