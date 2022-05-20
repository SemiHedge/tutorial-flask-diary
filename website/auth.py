from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/sign-in')
def sign_in():
    return "<p>Sign-In</p>"

@auth.route('/sign-out')
def sign_out():
    return "<p>Sign-Out</p>"

@auth.route('/sign-up')
def sign_up():
    return "<p>Sign-Up</p>"