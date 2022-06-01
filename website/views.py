from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    # POST : 메모 생성
    if request.method == "POST":
        title = request.form.get('note-title')
        content = request.form.get('note-content')

        if len(title) < 1 or len(content) < 1:
            flash("제목 또는 내용이 없습니다.", category = "error")
        elif len(title) > 50:
            flash("제목이 너무 깁니다. 50자 이내", category = "error")
        elif len(content) > 2000:
            flash("내용이 너무 깁니다. 2000자 이내", category="error")
        else :            
            # Note 인스턴스 생성 -> DB에 저장
            new_note = Note(title=title, content=content, user_id=current_user.id)    
            db.session.add(new_note)
            db.session.commit()

            flash("메모 생성 완료", category="success")
            return redirect(url_for('views.home')) # 없으면 메모 계속 생성


    return render_template('home.html', user=current_user)