from flask import Blueprint as Blueprint, render_template,request
from app.api.search_form import SearchForm
from app.api.all_engine_search import all_engines_data
from app.helpers.driver_script import check_search_query_exist

index = Blueprint('index', __name__, template_folder='templates')


@index.route('/')
def root_page():

    # res = []
    # all_data = all_engines_data('Avengers Endgame')
    # for data in all_data:
    #     res.append(data)

    return render_template('index.html', data=all)

@index.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    query = request.args.get('query')
    if check_search_query_exist(query):
        res = get_data(query)
        return render_template('search.html', title='Search', form=form, search_results=res,
                               query=form.searchbox.data)
    else:
        pass







