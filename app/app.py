from flask import Flask, Blueprint
from app.api.index import index_bp
app = Flask(__name__)

app.config['SECRET_KEY'] = 'any secret string'
app.register_blueprint(index_bp, url_prefix='/')


