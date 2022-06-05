from flask import Blueprint, redirect, render_template, request, flash, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import os
from werkzeug.utils import secure_filename

mypage_views = Blueprint('mypage_views', __name__)

# 나의 정보 페이지
@mypage_views.route('/', methods=['GET','POST'])
@login_required
def mypage():
    return render_template('mypage.html', user=current_user)


# 프로필 이미지 확장자 목록
ALLOWED_EXTENSIONS = ['png','jpg','jpeg','gif']

# 확장자 확인
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 나의 정보 수정 페이지
@mypage_views.route('/update', methods=['GET','POST'])
@login_required
def mypage_update():

    # 나의 정보 수정 요청 확인
    if request.method == 'POST':
        # 이미지 파일 정보가 있는 지 확인
        if 'imageFile' in request.files:
            image_file = request.files['imageFile']  # 디버그 모드로 확인

            # 허용된 파일 인지 확인
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                filetype = filename.rsplit('.', 1)[1].lower()
                image_path = f'{os.path.dirname(__file__)}/static/'  # ../website/static/

                # user id로 프로필 명 저장
                image_file.save(f'{image_path}{current_user.id}.{filetype}')
                
                # DB user.image_path에 반영
                user = User.query.get(current_user.id)
                user.image_path = f'{current_user.id}.{filetype}'
                db.session.commit()

                return redirect(url_for('mypage_views.mypage'))
            else:
                # 확장자가 허용되지 않음
                flash('이미지 파일은 png jpg jepg gif 만 지원합니다.', category = "error")
                return redirect(request.url)

        
    return render_template('mypage_update.html', user=current_user)
