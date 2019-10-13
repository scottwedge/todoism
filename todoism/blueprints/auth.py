from faker import Faker
from flask import render_template, redirect, url_for, Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_babel import _

from ..extensions import db
from ..models import User, Item

auth_bp = Blueprint('auth', __name__)
fake = Faker()


@auth_bp.route('/register')
def register():
    username = fake.user_name()
    while User.query.filter_by(username=username).first() is not None:
        username = fake.user_name()
    password = fake.word()
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    item = Item(body='Witness something truly majestic', author=user)
    item2 = Item(body='Help a complete stranger', author=user)
    item3 = Item(body='Drive a motorcycle on the Great Wall of China', author=user)
    item4 = Item(body='Sit on the Great Egyptian Pyrmids', done=True, author=user)
    db.session.add_all([item, item2, item3, item4])
    db.session.commit()

    return jsonify(username=username, password=password, message='Generate success.')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('todo.app'))

    if request.method == 'post':
        data = request.get_json()
        username = data['username']
        password = data['password']
        print('MMMMMMMMMMMMMMMMMMMMMMM')

        user = User.query.filter_by(username=username).first()

        if user is not None and user.validate_password(password):
            login_user(user)
            return jsonify(message='Login success.')
        return jsonify(message='Invalid username or password.'), 400
    return render_template('_login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify(message='Logout success.')
