import os

from databases import Database
from sanic import Sanic

from app.routes import setup_routes


def setup_database(app):
    app.db = Database(app.config.DB_URL)

    @app.listener('after_server_start')
    async def connect_to_db(*args, **kwargs):
        await app.db.connect()

    @app.listener('after_server_stop')
    async def disconnect_from_db(*args, **kwargs):
        await app.db.disconnect()


def create_app():
    app = Sanic(__name__)
    app.config.DB_URL = os.environ['DATABASE_URL']
    setup_database(app)
    setup_routes(app)

    parameters = {
        'host': '0.0.0.0',
        'port': int(os.environ.get('APP_PORT', 8000)),
        'debug': os.environ.get('APP_DEBUG', 'False').lower() == 'true'
    }
    workers = os.environ.get('APP_WORKERS', None)
    if workers:
        parameters['workers'] = workers
    app.run(**parameters)
