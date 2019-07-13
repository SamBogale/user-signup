from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user-signup:JfdroYHMJvBN8FFK@localhost:3306/user-signup'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'randomsecretkey'
db = SQLAlchemy(app)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(20))
    verify = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    def __init__(self, name,password,verify,email):
        self.name = name
        self.password = password
        self.verify = verify
        self.email = email
    def __repr__(self):
        return '<User %r>' % self.email

def is_email(email):
    at_index = email.find('@')
    if at_index < 0:
        return False
    
    dot_index = email.rfind('.')
    if dot_index < at_index:
        return False

    return True

@app.before_request


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name =request.form['text']
        password = request.form['password']
        verify = request.form['verify']
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if not is_email(email):
            flash("{} does not look like an email".format(email))
            return redirect('/')
        #else 
        #Save the user and do soemthing confirming the user is logged in
        user = User(name, password,verify,email)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.email
        return 'User is logged in'
    return render_template('register.html')


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