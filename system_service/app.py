from pathlib import Path

from flask import Flask
from flask_cors import CORS

from system_service.logger import load_logger

CORS_ALLOWED_ORIGINS_LIST = ["?"]

app = Flask(
    __name__,
    static_folder=str(Path(__file__).resolve().parents[1]/'static')
)

logger = load_logger(app)
api = None
db = None


def run(*args, **kwargs):
    from .database import database

    global api
    global db

    app.config['MONGODB_SETTINGS'] = {
        'host': 'mongodb+srv://tests:tests12345@cluster0-sf4tf.mongodb.net'
    }

    app.secret_key = '?'

    db = database.create(app)

    logger.info('[SERVICE] Started.')

    from .api import api

    api = api.create(app)

    CORS(app, origins=CORS_ALLOWED_ORIGINS_LIST, supports_credentials=True)

    app.run(*args, **kwargs)

