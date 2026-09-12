import ssl

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


# ==================================================
# Database Configuration
# ==================================================

DATABASE_URL = settings.database_url


if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured. "
        "Please add your PostgreSQL connection URL "
        "to the backend .env file."
    )


# ==================================================
# PostgreSQL Driver
# ==================================================

# Windows is blocking the psycopg2 native DLL on this
# system, so MediLens uses the pure-Python pg8000 driver.

if DATABASE_URL.startswith(
    "postgresql+psycopg2://"
):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql+psycopg2://",
        "postgresql+pg8000://",
        1,
    )

elif DATABASE_URL.startswith(
    "postgresql://"
):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+pg8000://",
        1,
    )


# ==================================================
# SSL Configuration
# ==================================================

# Local development:
# The current Windows environment is reporting a
# self-signed certificate in the certificate chain.
#
# Certificate verification can be enabled again
# before production deployment.

ssl_context = ssl.create_default_context()

ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


# ==================================================
# SQLAlchemy Engine
# ==================================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "ssl_context": ssl_context,
    },
)


# ==================================================
# Database Session
# ==================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# ==================================================
# Base Model
# ==================================================

class Base(DeclarativeBase):
    pass


# ==================================================
# Database Dependency
# ==================================================

def get_db():
    """
    Create a database session for an API request
    and close it after the request is completed.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()