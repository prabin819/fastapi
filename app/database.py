from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:krishna@localhost/fastapi'
engine = create_engine(SQLALCHEMY_DATABASE_URL) # The engine is resposible for establishing the connection to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)# to actually talk to the database, we make use of the session
Base = declarative_base()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()