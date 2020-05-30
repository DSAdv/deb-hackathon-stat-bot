import os
import psycopg2
from sqlalchemy import create_engine

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    user = os.environ['username']
    db_name = os.environ['db_name']
    port = os.environ['port']
    password = os.environ['password']
    host = os.environ['host']

    DB_URI = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}')
