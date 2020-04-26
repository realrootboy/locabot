from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from configs.database import config

class Database:
    engine = create_engine(
        config['dialect'] + '://' +
        config['user'] + ':' +
        config['password'] + '@' +
        config['host'] + ':' +
        config['port'] + '/' +
        config['database']
    )

    Session = sessionmaker(bind=engine)

    Base = declarative_base()

    test = "a"

    def __init__(self):
        return
