## 닉네임 비밀번호 변경
- 이메일의 경우도 할 수는 있겠지만, 보통 회원가입 시를 유지함
- models.py를 참고하면 닉네임은 중복이 되지 않도록(unique=True) 했음
    - `nickname = db.Column(db.String(80), unique=True, nullable=False)`
    - 중복 닉네임이 없는지 확인해야함

## 비밀번호 변경 HTML 추가하기
- 다른 페이지(sign_in.html, sing_up.html) 참고
```html
<div class="mb-3">
    <label for="InputPassword1" class="form-label">비밀번호</label>
    <input name="password1" type="password" class="form-control" id="InputPassword1"">
</div>
```

## 이메일은 변경 못하게 fieldset:disabled 추가
```html
<fieldset disabled="disabled">
    <div class="mb-3">
        <label for="InputEmail1" class="form-label">이메일</label>
        <input name="email" type="email" class="form-control" id="InputEmail1"
            aria-describedby="emailHelp" placeholder="{{ user.email }}">
    </div>
</fieldset>
```

## 닉네임, 비밀번호 관련 View 구현 - mypage_views.py
- 이미지, 닉네임, 비밀번호 중 변한 게 있는 지 확인하는 변수 `changed = False`
- 이미지 변경한 뒤 redirect하는 코드 삭제 `return redirect(url_for('mypage_views.mypage'))`
    - 대신 `changed = True`로 변경
- 닉네임, 비밀번호 관련하여 넘어온 값이 있는 지 확인하고 처리를 함
    - 이는 `auth.py`를 참고하여 구현

```python
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
        changed = False # 변경 여부가 있는 지 확인

        # 이미지 파일 정보가 있는 지 확인
        if 'imageFile' in request.files:
            image_file = request.files['imageFile']  # 디버그 모드로 확인

            # 파일이 존재하는지 확인
            if image_file.filename:
                # 허용된 파일인지 확인
                if allowed_file(image_file.filename):
                    filename = secure_filename(image_file.filename)
                    filetype = filename.rsplit('.', 1)[1].lower()
                    image_path = f'{os.path.dirname(__file__)}/static/'  # ../website/static/

                    # user id로 프로필 명 저장
                    image_file.save(f'{image_path}{current_user.id}.{filetype}')
                    
                    # DB user.image_path에 반영
                    user = User.query.get(current_user.id)
                    user.image_path = f'{current_user.id}.{filetype}'
                    db.session.commit()

                    changed = True
                else:
                    # 확장자가 허용되지 않음
                    flash('이미지 파일은 png jpg jepg gif 만 지원합니다.', category = "error")
                    return redirect(request.url)

        # 닉네임, 비밀번호 변경여부 확인
        nickname = request.form.get('nickname')
        password1 = request.form.get('password1')

        # 닉네임 입력 여부 및 유효성 검사
        if nickname:
            db_user = User.query.filter_by(nickname=nickname).first()
            if db_user :
                flash("이미 있는 닉네임입니다.")
                return redirect(request.url)
            elif len(nickname) < 2:
                flash("닉네임은 2자 이상입니다.", category="error")
                return redirect(request.url)
            else:
                user = User.query.get(current_user.id)
                user.nickname = nickname
                db.session.commit()
                changed = True
        
        # 패스워드 입력 여부 및 유효성 검사
        if password1:
            if len(password1) < 7:
                flash("비밀번호가 너무 짧습니다.", category = "error")
                return redirect(request.url)
            else:
                user = User.query.get(current_user.id)
                user.password = password1
                db.session.commit()
                changed = True
        
        # 변경사항이 있다면 redirect
        if changed:
            flash('정보가 변경 되었습니다', category = "success")
            return redirect(url_for('mypage_views.mypage'))
        else :
            flash('변경 사항이 없습니다.', category = "error")
            return redirect(request.url)
        
    return render_template('mypage_update.html', user=current_user)
```

## (선택)db에 적용하는 시점 일치
- db에 최종 적용하는 `db.session.commit()`
- 그런데 이미지, 닉네임, 비밀번호 중 하나라도 저장시 에러가 날 땐 처리를 안한다면 rollback을 적용하자.
    - `db.session.rollback()`
