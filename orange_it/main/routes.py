
from flask import render_template, request, Blueprint
from orange_it.models import Post, Thread

main = Blueprint('main', __name__)


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    threads = Thread.query.order_by(Thread.date_created.desc()).all()
    for thread in threads:
        print(thread.title)
    return render_template('index.html', posts=posts, threads=threads)


@main.route('/about')
def about():
    return '<h1>About Page<h1>'
