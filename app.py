from flask import Flask
from flask import render_template, request, url_for
from werkzeug.utils import redirect
from src.db_connection import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zz232323:zz232323@localhost/flaskmovie'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route("/")
def index():
    user_list = User.query.all()
    oneItem = User.query.filter_by(username="22").first()
    return render_template('user.html', myUser=user_list, oneItem=oneItem)


@app.route('/post_user', methods=['POST'])
def post_user():
    user = User(request.form['username'], request.form['email'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()

