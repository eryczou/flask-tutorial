from flask import Flask
from flask import render_template, request, url_for
from werkzeug.utils import redirect
from src.db_connection import db, User
from flask_sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zz232323:zz232323@localhost/flaskmovie'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True

# Create database connection object
db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Create a user to test with
# @app.before_first_request
# def create_user():
#     db.create_all()
#     user_datastore.create_user(email='matt@nobien.net', password='password')
#     db.session.commit()


# Views
@app.route('/')
@login_required
def home():
    return render_template('index.html')


@app.route('/profile/<id>')
@login_required
def profile(id):
    user = User.query.filter_by(id=id).first()
    return render_template('profile.html', pwd=user.password)

if __name__ == "__main__":
    app.run()

