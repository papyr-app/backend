from gevent import monkey
monkey.patch_all()

from app import init_app, socketio

app = init_app("config.ProductionConfig")
