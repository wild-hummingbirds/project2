from flask import Blueprint as Blueprint, render_template,request,flash
from app.api.search_form import SearchForm
from app.api.all_engine_search import all_engines_data
from app.helpers.main import data_dump

from app.helpers.sql_helper import get_data, check_search_query_exist

index_bp = Blueprint('index', __name__, template_folder='templates')


@index_bp.route('/',  methods=['GET', 'POST'])
def root():
    form = SearchForm()
    # res = []
    # all_data = all_engines_data('Avengers Endgame')
    # for data in all_data:
    #     res.append(data)
    all = [1,2,3,4]
    # print(form.validate_on_submit())
    # if form.validate_on_submit():
    #     q = form.searchbox.data
    #     q_exist = check_search_query_exist(q)
    #     if q_exist:
    #         res = get_data(q)
    #         return render_template('index.html', data=res, form=form, query=q)
    #     else:
    #         print("Searching....")
    #         data_dump(q)
    #         res = get_data(q)
    #         return render_template('index.html', data=res, form=form, query=q)
    # else:
    return render_template('index.html',form=form,valid_form=form.validate_on_submit())


@index_bp.route('/search', methods=['GET', 'POST'])
def search():
    all = [1, 2, 3, 4]
    res = "You searched for nothing"
    form = SearchForm()
    q = form.searchbox.data.lower()
    if form.validate_on_submit():
        q_exist = check_search_query_exist(q)
        if q_exist:
            res = get_data(q)
            return render_template('index.html', data=res, form=form, query=q, valid_form=form.validate_on_submit())
        else:
            print("Searching....")
            data_dump(q)
            res = get_data(q)
            return render_template('index.html', data=res, form=form, query=q, valid_form=form.validate_on_submit())
    flash('No Search Query Provided', 'error')
    return render_template('index.html', form=form, query=q, valid_form=form.validate_on_submit())

    # query = request.args.get('query')
    # if check_search_query_exist(query):
    #
    #     res = get_data(query)
    #     return render_template('search.html', title='Search', form=form, search_results=res,
    #                            query=form.searchbox.data)
    # else:
    #     pass




@index_bp.route('/about')
def about():
    return render_template('about.html')




