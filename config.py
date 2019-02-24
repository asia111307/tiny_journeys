class DevelopmentConfig(object):
    # db = abstract_db.connect(config.DB_IP, config.DB_PORT, config.DB_LOGIN, config.DB_PASS)
    DB_NAME = 'gr_db'
    DB_PATH = '.temp/gr.db'
    DB_IP = "127.0.0.1"
    DB_PORT = 5061
    DB_LOGIN = "admin"
    DB_PASS = "p@ssw0rd"

    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 80

    DEBUG = True
    ENV = 'development'

    SQLITE_DB_NAME = 'gr_db'
    SQLITE_PATH = '.temp/gr_db.db'