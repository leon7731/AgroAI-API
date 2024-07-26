# Config Folder
from Config.Config import settings

# SQL Alchemy Lib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PostgresSQL_UserName = settings.postgres_user
PostgresSQL_Password = settings.postgres_password
PostgresSQL_IPAddress = settings.postgres_ipaddress
PostgresSQL_Port = settings.postgres_port
PostgresSQL_DatabaseName = settings.postgres_db_name


# # Local Database Testing
# SQLALCHEMY_DATABASE_URL = f"postgresql://{PostgresSQL_UserName}:{PostgresSQL_Password}@{PostgresSQL_IPAddress}:{PostgresSQL_Port}/{PostgresSQL_DatabaseName}"

# Docker Database Testing
SQLALCHEMY_DATABASE_URL = f"postgresql://{PostgresSQL_UserName}:{PostgresSQL_Password}@postgres:{PostgresSQL_Port}/{PostgresSQL_DatabaseName}"


Engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
Base = declarative_base()
### Create a database session ### 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
