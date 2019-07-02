from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user-signup:JfdroYHMJvBN8FFK@localhost:3306/user-signup'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    password = db.Column(db.String(20))
    verify = db.Column(db.String(8))
    email = db.Column(db.String(120), unique=True)

    

    def __init__(self, name,password,verify,email):
        self.name = name
        self.password = password
        self.verify = verify
        self.email = email



tasks = []
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name =request.form['text']
        password = request.form['password']
        verify = request.form['verify']
        email = request.form['email']
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(name, password,verify,email)
            db.session.add(new_user)
            db.session.commit()
            
            return redirect('/')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_name = request.form['user']
        new_task = User(task_name)
        db.session.add(new_task)
        db.session.commit()
    return render_template('register.html',title="User Signup!")


if __name__ == '__main__':
    app.run()