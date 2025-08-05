from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:krishna@localhost/fastapi'
engine = create_engine(SQLALCHEMY_DATABASE_URL) # The engine is resposible for establishing the connection to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)# to actually talk to the database, we make use of the session
Base = declarative_base()

# declarative_base() is a function provided by SQLAlchemy that creates a base class for your database models to inherit from.

# Why we need it
# In SQLAlchemy's Object Relational Mapping (ORM), we define tables as Python classes.

# But for those classes to be recognized by SQLAlchemy as tables, they must inherit from a special base class — and that's what declarative_base() gives you.

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time       
# # database connection (psycopg)
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='krishna', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('database connection was successful')
#         break
#     except Exception as error:
#         print('Connection to database failed.')
#         print('Error: ', error)
#         time.sleep(3)