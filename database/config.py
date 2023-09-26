import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

dotenv_path = "../.env"
load_dotenv(dotenv_path)
engine = create_engine(
    f'postgresql://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASSWORD")}@{os.environ.get("DB_HOST")}/{os.environ.get("DB_NAME")}'
)

Base = declarative_base()

Session = sessionmaker()
