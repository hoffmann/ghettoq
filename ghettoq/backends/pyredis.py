from redis import Redis as Redis
from ghettoq.backends.base import BaseBackend

DEFAULT_PORT = 6379
DEFAULT_DB   = 0

class RedisBackend(BaseBackend):

    def __init__(self, host=None, port=None, user=None, password=None,
            database=None, timeout=None):
        
        if type(database) != int:
            if not database or database == "/":
                database = DEFAULT_DB
            elif database.startswith('/'):
                try:
                     database = int(database[1:])
                except ValueError:
                     raise AttributeError('Database name must be integer between 0 and database_count - 1')
            else:
                try:
                     database = int(database)
                except ValueError:
                     raise AttributeError('Database name must be integer between 0 and database_count - 1')
        
        super(RedisBackend, self).__init__(host, port, user, password, database, timeout)
        
    def establish_connection(self):
        self.port = self.port or DEFAULT_PORT
        return Redis(host=self.host, port=self.port, db=self.database,
                     password=self.password)

    def put(self, queue, message):
        self.client.lpush(queue, message)

    def get(self, queue):
        return self.client.rpop(queue)

    def purge(self, queue):
        return self.client.delete(queue)
