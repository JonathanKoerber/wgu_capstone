
from orange_it import create_app, db
from orange_it.config import DevelopmentConfig

app = create_app(DevelopmentConfig)
app.app_context().push()
db.init_app(app)
db.drop_all()
db.create_all()
print('init db')
