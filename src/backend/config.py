import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'db'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'database': os.getenv('DB_NAME', 'dompetku'),
    'user': os.getenv('DB_USER', 'dompetku_user'),
    'password': os.getenv('DB_PASSWORD', 'dompetku_pass')
}

# App configuration
APP_PORT = int(os.getenv('APP_PORT', 5000))
APP_DEBUG = os.getenv('APP_DEBUG', 'true').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')

# Initialize SQLAlchemy
db = SQLAlchemy()
