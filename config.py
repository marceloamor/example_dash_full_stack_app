import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database configuration
SQLITE_DB_PATH = os.path.join(BASE_DIR, 'todo.db')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{SQLITE_DB_PATH}')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Application settings
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-development-only')

# Dash settings
DASH_TITLE = 'To-Do Application'
DASH_UPDATE_INTERVAL = 5000  # milliseconds
