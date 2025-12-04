from flask import Blueprint, jsonify
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy import text
from ..extensions import db

home_bp = Blueprint("home", __name__, url_prefix="")

@home_bp.route("/")
def home():
    return {"message": "this is home route"}, 200

# Health check endpoint for database status
@home_bp.route("/db")
def health():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "ok", "database": "connected"}), 200
    except (OperationalError, SQLAlchemyError):
        return jsonify({"status": "error", "database": "down"}), 503
