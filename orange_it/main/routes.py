
from flask import render_template, url_for, redirect, request, \
    Blueprint, g, current_app
from orange_it.models import Post
from orange_it.models import Thread


main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.date_posted.desc())
    threads = Thread.query.order_by(Thread.date_created.desc()).all()

    return render_template('index.html', posts=posts, threads=threads)

@main.route('/search', methods=['GET', 'POST'])
def search():
    page = request.args.get('page', 1, type=int)

    num_posts = min(request.args.get('limit', 50), 50)
    search_str = request.args.get('query', '')
    posts = Post.query.search(search_str, num_posts)

    threads = Thread.query.order_by(Thread.date_created.desc()).all()
    return render_template('index.html', title=('Search'), posts=posts, threads=threads,
                           next_url=next_url, prev_url=prev_url)
   # return render_template('index.html', posts=posts, threads=threads)

@main.route('/about')
def about():
    return '<h1>About Page<h1>'
