from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import DB_SETTINGS as db

SQLALCHEMY_DATABASE_URL = "postgresql://{user}:{password}@{address}/{name}".format(
    user=db.user, password=db.password, address=db.address, name=db.name
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
