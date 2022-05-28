from flask import Blueprint, redirect, render_template, request, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    return render_template('sign_in.html')

@auth.route('/sign-out')
def sign_out():
    return render_template('sign_out.html')

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # form - input의 name 속성을 기준으로 가져오기
        email = request.form.get('email')
        nickname = request.form.get('nickname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 유효성 검사
        if len(email) < 5 :
            flash("이메일은 5자 이상입니다.", category="error")
        elif len(nickname) < 2:
            flash("닉네임은 2자 이상입니다.", category="error")
        elif password1 != password2 :
            flash("비밀번호와 비밀번호재입력이 서로 다릅니다.", category="error")
        elif len(password1) < 7:
            flash("비밀번호가 너무 짧습니다.", category="error")
        else:
            # Create User > DB
            new_user = User(email=email, nickname=nickname, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("회원가입 완료.", category="success")  # Create User -> DB
            return redirect(url_for('views.home'))

    return render_template('sign_up.html')