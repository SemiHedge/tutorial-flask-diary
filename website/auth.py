from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/sign-in')
def sign_in():
    return render_template('sign_in.html')

@auth.route('/sign-out')
def sign_out():
    return render_template('sign_out.html')

@auth.route('/sign-up')
def sign_up():
    return render_template('sign_up.html')