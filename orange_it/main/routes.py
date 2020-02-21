
from flask import render_template, request, Blueprint
from orange_it.main.forms import SearchForm
from orange_it.models import Post, Thread

from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from orange_it import db
from orange_it.models import Rule, Thread
from orange_it.rules.forms import (RuleForm)
main = Blueprint('main', __name__)


@main.route('/')
def index():
    form = SearchForm()
    if form.validate_on_submit():
        search_string = form.search.data
        search_results(search_string)
        print(search_string)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    threads = Thread.query.order_by(Thread.date_created.desc()).all()
    return render_template('index.html', posts=posts, threads=threads, form=form)

# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     searchForm = searchForm()
#     courses = models.Course.query
#
#     if searchForm.validate_on_submit():
#         courses = courses.filter(models.Course.name.like('%' + searchForm.courseName.data + '%'))
#
#     courses = courses.order_by(models.Course.name).all()
#
#     return render_template('courselist.html', courses = courses)

@main.route('/results/<string:search>', methods=['GET', 'POST'])
def search_results(search):
    search_string = search.data['search']
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.title == search_string).paginate(page=page, per_pate=5)
    if not posts:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        threads = Thread.query.order_by(Thread.date_created.desc()).all()
        return render_template('index.html', posts=posts, threads=threads)

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    threads = Thread.query.order_by(Thread.date_created.desc()).all()
    return render_template('index.html', posts=posts, threads=threads)

@main.route('/about')
def about():
    return '<h1>About Page<h1>'
