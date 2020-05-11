from orange_it import create_app
from orange_it.config import Config, DevelopmentConfig

app = create_app(DevelopmentConfig)
if __name__ == '__main__':
    app.run(debug=True)

