import os
import psycopg2

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    token = os.environ.get('token')
    conn = psycopg2.connect(dbname=os.environ.get('dbname'), user=os.environ.get('user'),
                            password=os.environ.get('password'), host=os.environ.get('host'))

