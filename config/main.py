"""
    This module contains the configuration classes for the project.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """
    Base configuration class. Contains all the default configurations.
    """

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    DATABASE_USER: str = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT")
    SQLALCHEMY_DATABASE_URL: str = (
        f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@"
        f"{DATABASE_URL}:{DATABASE_PORT}/{DATABASE_NAME}"
    )


config = Config()
