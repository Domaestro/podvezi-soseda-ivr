import os

from app import create_app

app = create_app()
app.config.from_object(os.environ['APP_SETTINGS'])

if __name__ == '__main__':
    app.run()