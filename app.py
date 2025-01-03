from flask import Flask
from database.database import db
from database.config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
