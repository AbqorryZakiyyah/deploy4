from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, request
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
            return jsonify({'status': 'success', 'message': 'Login berhasil'}), 200
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return jsonify({'status': 'success', 'message': 'Login berhasil'}), 200
                #return redirect(url_for('views.home'))

            else:
                flash('Incorrect password, try again.', category='error')
                return jsonify({'status': 'error', 'message': 'Incorrect password'}), 400
        else:
            flash('Email does not exist.', category='error')
            return jsonify({'status': 'error', 'message': 'Email does not exist.'}), 400
    
    #return render_template("login.html", user=current_user)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'status': 'success', 'message': 'Logout berhasil'}), 200


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
            return jsonify({'status': 'success', 'message': 'Sign up berhasil'}), 200
    elif request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
            return jsonify({'status': 'error', 'message': 'Email already exists.'}), 400
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
            return jsonify({'status': 'error', 'message': 'Email must be greater than 3 characters.'}), 400
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
            return jsonify({'status': 'error', 'message': 'First name must be greater than 1 character.'}), 400
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
            return jsonify({'status': 'error', 'message': 'Passwords don\'t match.'}), 400
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
            return jsonify({'status': 'error', 'message': 'Password must be at least 7 characters.'}), 400
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return jsonify({'status': 'success', 'message': 'Registrasi Berhasil'}), 200

    #return render_template("sign_up.html", user=current_user)

