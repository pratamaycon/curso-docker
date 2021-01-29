import os
import psycopg2
import redis
import json
from bottle import Bottle, request

class Sender(Bottle):
    def __init__(self):
        super().__init__()
        
        db_host = os.getenv('DB_HOST', 'db')
        db_user = os.getenv('DB_USER', 'postgres')
        db_name = os.getenv('DB_NAME', 'sender')
        dsn = f'dbname={db_name} user={db_user} host={db_host}'
        self.conn = psycopg2.connect(dsn)

        redis_host = os.getenv('REDIS_HOST', 'queue')
        self.fila = redis.StrictRedis(host=redis_host, port=6379, db=0)

        self.route('/', method='POST', callback=self.send)