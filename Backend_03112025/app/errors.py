from flask import jsonify  # Used to return JSON responses
from marshmallow import ValidationError  # To catch validation errors from Marshmallow schemas
from sqlalchemy.exc import OperationalError, SQLAlchemyError

def register_error_handlers(app):
    """
    Register global error handlers for the Flask app.
    This helps to return consistent JSON responses for different errors.
    """

    # -------------------------------
    # Handle Marshmallow validation errors
    # -------------------------------
    @app.errorhandler(ValidationError)
    def handle_marshmallow(err):
        """
        Triggered automatically when Marshmallow schema validation fails.
        Returns:
            - JSON object with 'errors' key containing validation messages
            - HTTP status code 400 (Bad Request)
        """
        return jsonify({"errors": err.messages}), 400

    # -------------------------------
    # Handle generic 400 Bad Request errors
    # -------------------------------
    @app.errorhandler(400)
    def bad_request(e):
        """
        Triggered for generic HTTP 400 errors not caught by Marshmallow.
        Returns:
            - JSON object with error message
            - HTTP status code 400
        """
        return jsonify({"error": "Bad request"}), 400

    # -------------------------------
    # Handle 404 Not Found errors
    # -------------------------------
    @app.errorhandler(404)
    def not_found(e):
        """
        Triggered when a requested route or resource does not exist.
        Returns:
            - JSON object with error message
            - HTTP status code 404
        """
        return jsonify({"error": "Not found"}), 404

    # -------------------------------
    # Handle 500 Internal Server Error
    # -------------------------------
    @app.errorhandler(500)
    def server_error(e):
        """
        Triggered for unhandled exceptions in the app.
        Returns:
            - JSON object with error message
            - HTTP status code 500
        """
        return jsonify({"error": "Server error"}), 500

    # -------------------------------
    # Handle 503 Database connection failed
    # -------------------------------
    @app.errorhandler(OperationalError)
    def handle_db_connection_error(e):
        return jsonify({"error": "Database connection failed. Please try again later."}), 503

    # -------------------------------
    # Handle 500 Database Error
    # -------------------------------
    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(e):
        return jsonify({"error": "A database error occurred"}), 500

    # ✅ Catch ANY other unhandled runtime exceptions
    @app.errorhandler(Exception)
    def handle_unexpected_error(err):
        # Log error on console or log file
        print(f"Unexpected error: {err}")
        return jsonify({"error": "Something went wrong"}), 500