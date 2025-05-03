import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, redirect, url_for
from src.models.models import db
from src.routes.animal_routes import animal_bp

app = Flask(__name__, static_folder=\"static\", template_folder=\"templates\")
app.config[\"SECRET_KEY\"] = os.urandom(24) # Needed for flash messages

# --- Database Configuration ---
# Use environment variables for sensitive data is best practice, but using defaults here for simplicity.
DB_USERNAME = os.getenv(\"DB_USERNAME\", \"root\")
DB_PASSWORD = os.getenv(\"DB_PASSWORD\", \"password\")
DB_HOST = os.getenv(\"DB_HOST\", \"localhost\")
DB_PORT = os.getenv(\"DB_PORT\", \"3306\")
DB_NAME = os.getenv(\"DB_NAME\", \"mydb\")

# Uncomment and configure the database URI
app.config[\"SQLALCHEMY_DATABASE_URI\"] = f\"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}\"
app.config[\"SQLALCHEMY_TRACK_MODIFICATIONS\"] = False

# Initialize extensions
db.init_app(app)

# Register blueprints
app.register_blueprint(animal_bp)

# Create database tables if they don\"t exist
with app.app_context():
    # Before creating tables, let's ensure the database itself exists.
    # This basic check might require manual DB creation or more robust logic.
    # For now, we assume 'mydb' exists on the MySQL server.
    # We also need to execute the schema.sql manually first to create the tables
    # OR use db.create_all() if models cover the entire schema.
    # Since our models might not cover everything (like Abrigos fully), manual schema execution is safer.
    # db.create_all() # Use this if models.py defines ALL tables needed.
    # It's safer to instruct the user (or do it via shell) to run schema.sql first.
    pass # Assuming schema.sql was run manually or via another step.

# Redirect root URL to the animal consultation page
@app.route(\"/\")
def index():
    # Redirect to the main consultation page
    return redirect(url_for(\"animal.consultar_animal\"))

if __name__ == \"__main__\":
    # Listen on all interfaces, important for deployment/exposure
    app.run(host=\"0.0.0.0\", port=5000)

