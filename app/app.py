from flask import Flask, Blueprint
from app.api.index import index
app = Flask(__name__)


app.register_blueprint(index, url_prefix='/')


