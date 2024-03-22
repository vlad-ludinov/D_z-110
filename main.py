from flask import Flask, render_template, request, url_for, redirect, make_response
from flask_wtf.csrf import CSRFProtect
from models import db, User
from forms import RegistrationForm, DeleteForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = b'ba9dc9cda3ef2702d8bf8d177b1b6708984e145835aef6d8bd8f516647101dcc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
bcrypt = Bcrypt(app)


csrf = CSRFProtect(app)
# pip install Flask-SQLAlchemy
# pip install Flask-WTF
# pip install flask-bcrypt


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/hello/<name>', methods=['GET', 'POST'])
def hello(name):

    form = DeleteForm()

    user = User.query.filter_by(name=name).first()

    user_data = {'name': user.name, 'surname': user.surname,
                 'email': user.email, 'password': user.password}

    if request.method == 'POST':
        if request.form.get('delete_button'):
            response = redirect(url_for('registration'))
            db.session.delete(user)
            db.session.commit()

            return response

    return render_template('hello.html', **user_data, form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, surname=surname, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        response = redirect(url_for('hello', name=name))
        response.set_cookie('name', name)
        return response
        # return redirect(url_for('hello'))
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
