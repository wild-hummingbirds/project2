from flask import Blueprint as Blueprint, render_template

from app.api.all_engine_search import all_engines_data
from app import app
index = Blueprint('index', __name__, template_folder='templates')


@app.route('/')
@app.route('/index')
def root_page():

    res = []
    all_data = all_engines_data('Avengers Endgame')
    for data in all_data:
        res.append(data)

    all = [1, 2, 3, 4, 555,100]
    return render_template('index.html', data=res)
