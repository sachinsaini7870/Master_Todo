import os
from dotenv import load_dotenv

load_dotenv()



class BaseConfig:
    """
    Base configuration used by all environments (development, testing, production).
    This class stores all common settings for the entire Flask application.
    """

    # --------------------------
    # ✅ SECURITY SETTINGS
    # --------------------------
    # SECRET_KEY is used by Flask to securely sign session cookies
    # and protect against tampering, CSRF attacks, etc.
    # This should always be overridden with a strong value in production.
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # --------------------------
    # ✅ DATABASE SETTINGS
    # --------------------------
    # SQLALCHEMY_DATABASE_URI tells SQLAlchemy which database to connect to.
    # The value is taken from environment variable DATABASE_URL.
    # If not provided, it falls back to a local SQLite file (app.db).
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")

    # Disables SQLAlchemy's event system that tracks object changes.
    # This feature slows down performance and is unnecessary for most apps.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --------------------------
    # ✅ JWT TOKEN SETTINGS
    # --------------------------
    # JWT_SECRET_KEY is used to sign and verify JWT access tokens.
    # Must be a strong secret in production to prevent token hacking.
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # --------------------------
    # ✅ LOGGING SETTINGS
    # --------------------------
    # LOG_LEVEL controls how much information is shown in logs.
    # Common values: DEBUG, INFO, WARNING, ERROR.
    LOG_LEVEL = "INFO"

    # --------------------------
    # ✅ RESTX / SWAGGER SETTINGS
    # --------------------------
    # RESTX_MASK_SWAGGER controls whether Swagger hides fields behind masks.
    # Setting this to False ensures Swagger shows ALL fields clearly,
    # making API documentation easier to read in all environments.
    RESTX_MASK_SWAGGER = False   # Disable mask fields (clean output)
    SWAGGER_UI_DOC_EXPANSION = "none"

    # --------------------------
    # ✅ GENERAL APP SETTINGS
    # --------------------------
    # Name of your application (used in logs, documentation, metadata, etc.)
    APP_NAME = "Flask Todo App"

    # DEBUG mode reloads server automatically and shows detailed error pages.
    # OFF in production for security.
    DEBUG = False

    # When TESTING is True, Flask enables testing mode (no error catching).
    TESTING = False

    # Ensures Flask re-throws errors instead of hiding them.
    # Useful for debugging and for proper error logging.
    PROPAGATE_EXCEPTIONS = True





class DevelopmentConfig(BaseConfig):
    """
    Configuration used when developing the application locally.
    This setup is helpful for debugging and building new features.
    """

    # Enables Flask debug mode → auto reload + detailed error pages.
    DEBUG = True

    # Shows detailed logs to help developers understand what's happening.
    LOG_LEVEL = "DEBUG"

    # When True: prints raw SQL queries to console.
    # Very useful for debugging database queries. Off by default.
    SQLALCHEMY_ECHO = False
    
    # Dev-specific Swagger features
    RESTX_MASK_SWAGGER = False
    SWAGGER_UI_DOC_EXPANSION = "list"  # Expand API routes for easy browsing


class ProductionConfig(BaseConfig):
    """
    Configuration used when the app is deployed live on a server.
    This setup focuses on security, performance, and stability.
    """

    # Debug mode MUST be off in production for security reasons.
    DEBUG = False

    # Show only important warnings and errors in logs.
    LOG_LEVEL = "WARNING"

    # Production database MUST come from environment variable.
    # We override BaseConfig here to force real DB usage.
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    
    # In production, API docs should be OFF or restricted
    RESTX_MASK_SWAGGER = False
    SWAGGER_UI_DOC_EXPANSION = "none"  # Hide extra details


class TestingConfig(BaseConfig):
    """
    Configuration used for automated unit tests.
    This creates a clean, temporary environment for each test run.
    """

    # Enable testing mode → exceptions propagate, better error visibility.
    TESTING = True

    # Debug mode also ON during tests for more information.
    DEBUG = True

    # Use an in-memory database (stored in RAM).
    # Fast, isolated, and automatically resets after tests.
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    
    # Swagger usually not needed
    RESTX_MASK_SWAGGER = False


# ---------------------------------------
# ✅ CONFIG MAP (Used by app factory)
# ---------------------------------------
# This dictionary helps the app factory select the correct configuration
# based on the environment name such as:
# app = create_app("development")
# app = create_app("production")
# app = create_app("testing")
config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
