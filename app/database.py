from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

MYSQL_USER = "root"
MYSQL_PASSWORD = "password"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DB = "retaildb"  # ⚠️ must match name you used in docker run

DATABASE_URL = (
    f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
