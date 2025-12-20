"""Application configuration."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Base configuration class."""

    # Application
    APP_NAME = os.getenv('APP_NAME', 'Church ERP')
    APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
    APP_PORT = int(os.getenv('APP_PORT', '8000'))
    APP_DEBUG = os.getenv('APP_DEBUG', 'False').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'church_erp')
    DB_USER = os.getenv('DB_USER', 'church_erp_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')

    # PostgreSQL superuser credentials (for database creation)
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '')

    # Connection Pool Settings
    DB_POOL_MIN = int(os.getenv('DB_POOL_MIN', '2'))
    DB_POOL_MAX = int(os.getenv('DB_POOL_MAX', '10'))

    # Redis Configuration (if needed later)
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_DB = int(os.getenv('REDIS_DB', '0'))

    # Security
    PASSWORD_MIN_LENGTH = 8
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = not APP_DEBUG  # Only over HTTPS in production
    SESSION_COOKIE_SAMESITE = 'Lax'
    MAX_LOGIN_ATTEMPTS = 5
    ACCOUNT_LOCK_DURATION_MINUTES = 30

    # File Upload
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {
        'pdf', 'doc', 'docx', 'xls', 'xlsx',
        'jpg', 'jpeg', 'png', 'gif',
        'txt', 'csv'
    }

    # Email Configuration (if needed)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.example.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@church.org')

    # Pagination
    ITEMS_PER_PAGE = 50
    MAX_ITEMS_PER_PAGE = 100

    @classmethod
    def init_app(cls):
        """Initialize application with configuration."""
        # Create upload folder if it doesn't exist
        cls.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_database_url(cls):
        """Get database connection URL."""
        return (
            f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}"
            f"@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
        )


class DevelopmentConfig(Config):
    """Development configuration."""
    APP_DEBUG = True
    DB_NAME = os.getenv('DB_NAME', 'church_erp_dev')


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DB_NAME = os.getenv('DB_NAME', 'church_erp_test')


class ProductionConfig(Config):
    """Production configuration."""
    APP_DEBUG = False

    @classmethod
    def init_app(cls):
        """Initialize production configuration."""
        super().init_app()

        # Ensure secret key is set in production
        if cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError("SECRET_KEY must be set in production environment!")


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """
    Get configuration for specified environment.

    Args:
        env: Environment name ('development', 'testing', 'production')
             If None, uses APP_ENV environment variable or 'default'

    Returns:
        Configuration class
    """
    if env is None:
        env = os.getenv('APP_ENV', 'default')

    return config.get(env, config['default'])
