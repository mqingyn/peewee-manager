# peewee-manager
peewee db connection manager

### version: 1.0

* pip: [peewee-manager](https://pypi.python.org/pypi/peewee-manager)
* Install: pip install peewee-manager
* Getting Started:
  
        from peeweemgr.database import DBManager

        DATABASE = {
              'default': {
                  'master': {
                      'name': 'test',
                      'user': 'root',
                      'host': '127.0.0.1',
                      'passwd': '',
                      'port': 3306,
                      'engine': 'MySQLDatabase',
                      'pool': 'PooledMySQLDatabase',
                      'pool_args': {
                          'max_connections': 50,
                          'stale_timeout': 200
                      },
                      # 'echo': True
                  },
                  # slave read-only db config list, if you have.
                  'replica': [{
                      'name': 'test',
                      'user': 'root',
                      'host': '127.0.0.1',
                      'passwd': '',
                      'port': 3307,
                      'engine': 'MySQLDatabase',
                      'pool': 'PooledMySQLDatabase',
                      'pool_args': {
                          'max_connections': 50,
                          'stale_timeout': 200
                      },
                      # 'echo': True
                  },
                      {
                      'name': 'test',
                      'user': 'root',
                      'host': '127.0.0.1',
                      'passwd': '',
                      'port': 3308,
                      'engine': 'MySQLDatabase',
                      'pool': 'PooledMySQLDatabase',
                      'pool_args': {
                          'max_connections': 50,
                          'stale_timeout': 200
                      },
                      # 'echo': True
                  }]
              }
          }
        db = DBManager(DATABASE)
        
        # start creating models
        class Blog(db.Model):
            # this model will automatically work with the database specified
            # in the application's config.
        
        
