## 마이페이지 관련 View 생성 - mypage_views.py
- `views.py` 또는 `auth.py`를 참고하여 기초 `mypage_views.py`를 작성

```python
from flask import Blueprint, redirect, render_template, request, flash, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db

mypage_views = Blueprint('mypage_views', __name__)

# 나의 정보 페이지
@mypage_views.route('/mypage', methods=['GET','POST'])
@login_required
def mypage():
    return render_template('mypage.html')


# 나의 정보 수정 페이지
@mypage_views.route('/mypage/update', methods=['GET','POST'])
@login_required
def mypage_update():
    return render_template('mypage_update.html')
```
- blueprint 이름 : `mypage_views`
- route : `/mypage`, `/mypage/update`
- 둘 다 로그인 필수 페이지이니 
    - `@login_required`


### Blueprint 등록 - __init__.py
```python
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'semicircle_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # 블루프린트 인스턴스 가져오기
    from .views import views
    from .auth import auth
    from .mypage_views import mypage_views

    # 플라스크 앱에 등록하기
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(mypage_views, url_prefix='/')

    # DB에 사용할 모델 불러오기
    from .models import User, Note  # from .models import *
    create_database(app)

    # flask-login 적용
    login_manager = LoginManager()
    login_manager.login_view = 'auth.sign_in'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)  # primary_key

    # Flask-Migrate 적용
    migrate = Migrate(app, db, render_as_batch=True)

    return app
```
- 블루프린트 추가 : `from .mypage_views import mypage_views`
- 플라스크 앱에 적용 : `app.register_blueprint(mypage_views, url_prefix='/')`

### (선택) url_prefix 사용하기
- 일부러 `/mypage`, `mypage/update` 로 하여 공통 경로를 가지게해봤다.
- 이 경우 다음처럼 변경할 수 있다.
- `__init__.py` : `app.register_blueprint(mypage_views, url_prefix='/mypage')`
- `mypage_views.py`
    - `@mypage_views.route('/', methods=['GET','POST'])`
    - `@mypage_views.route('/update', methods=['GET','POST'])`



## 기본 템플릿 만들기 - mypage.html
```html
<!-- mypage.html -->
{% extends "base.html" %}

{% block title %}Title - Mypage{% endblock %}

{% block content %}
<h2>나의 정보</h2>
{{user.image_path}}
<label for="">{{ user.nickname }}</label>
<label for="">{{ user.email }}</label>
<a href="/mypage/update"><button>정보 수정</button></a>
{% endblock %}
```
- {{user.image_path}} 가 None이 나온다.

### 기본 프로필 /static에 넣기
- `basic_profile.png`
    - DB에 user의 image_path가 NULL일 때, 'basic_profile.png`로 대체한다.
        - 초기 개발 때 Models.py에서 `image_path`의 default로 변경했으면 더 좋았을 것 같기도?
        - 그 데이터도 아깝다면 지금처럼 NULL로 두는 것도 방법.

### 기본 프로필 적용 jinja 문법
- jinja 템플릿 `url_for`를 이용
    - [ref. Adding a favicon](https://flask.palletsprojects.com/en/2.1.x/patterns/favicon/?highlight=url_for#adding-a-favicon)
    - `<img src="{{ url_for('static', filename=파일명)}}">`

```html
<!-- mypage.html -->
{% extends "base.html" %}

{% block title %}Title - Mypage{% endblock %}

{% block content %}
<h2>나의 정보</h2>
{% if user.image_path %}
    <img src="{{ url_for('static', filename=user.image_path)}}" alt="사용자프로필이미지">
{% else %}
    <img src="{{ url_for('static', filename='basic_profile.png')}}" alt="기본프로필이미지">
{% endif %}

<label for="">{{ user.nickname }}</label>
<label for="">{{ user.email }}</label>
<a href="/mypage/update"><button>정보 수정</button></a>
{% endblock %}
```

### 직접 확인하기
- mypage에 다음 사항 확인
    - 기본 사진
    - 나의 이름 / 이메일
    - 정보 수정 버튼 이동

### 나의 정보 조회 페이지 꾸미기 - mypage.html
- Bootstrap 문서를 참고하며 꾸미기
    - [ref. Form > DisabledForm](https://getbootstrap.com/docs/5.2/forms/overview/#disabled-forms)
        - 나의 수정 페이지에서 활용할 것이기 때문에 해당 폼을 참조
        - 회원 가입 때도 비슷하게 구현했으니, sign_up.html을 참조하자.
    - [ref. Image > Aligning images](https://getbootstrap.com/docs/5.2/content/images/#aligning-images)
- 레이아웃 사이즈도 정해보자
    - [ref. Layout > Horizontal](https://getbootstrap.com/docs/5.2/layout/columns/#horizontal-alignment)
    - [ref. Layout > Grid](https://getbootstrap.com/docs/5.2/layout/grid/#grid-options)

```html
<!-- mypage.html -->
{% extends "base.html" %}

{% block title %}Title - Mypage{% endblock %}

{% block content %}

<div class="container">
    <div class="row justify-content-center">
        <div class="col-sm-6">
            <form method="GET" action="/mypage/update">
                <fieldset disabled="disabled">
                    <h2 align="center">MyPage</h2>

                    <!-- 프로필 이미지 영역 -->
                    {% if user.image_path %}
                    <img src="{{ url_for('static', filename=user.image_path)}}" alt="사용자프로필이미지"
                        class="rounded mx-auto d-block">
                    {% else %}
                    <img src="{{ url_for('static', filename='basic_profile.png')}}" alt="기본프로필이미지"
                        class="rounded mx-auto d-block">
                    {% endif %}

                    <!-- 기본 정보 영역 -->
                    <div class="mb-3">
                        <label for="InputEmail1" class="form-label">이메일</label>
                        <input name="email" type="email" class="form-control" id="InputEmail1"
                            aria-describedby="emailHelp" placeholder="{{ user.email }}">
                    </div>

                    <div class="mb-3">
                        <label for="Nickname1" class="form-label">닉네임</label>
                        <input name="nickname" type="text" class="form-control" id="Nickname1"
                            placeholder="{{ user.nickname }}">
                    </div>

                </fieldset>
                <button type="submit" class="btn btn-primary">정보 수정</button>
            </form>
        </div>
    </div>
</div>

{% endblock %}
```
- `div.container > div.row.justify-content-center > div.col-sm-6` 로 레이아웃 잡기
- `내부는 sign_up.html 참조`
- 양 옆 margin-auto로 잡아주는 부트스트랩 class`mx-auto`
    - CSS 기초를 안다면 바로 이해할 것
- `fieldset:disabled`로 비활성 영역 생성
- `form`의 `method:GET, action:/mypage/update`로 속성 설정


## 나의 정보 수정 페이지 생성 - mypage_update.html
```html
<!-- mypage_update.html -->
{% extends "base.html" %}

{% block title %}Title - Mypage 수정{% endblock %}

{% block content %}

<div class="container">
    <div class="row justify-content-center">
        <div class="col-sm-6">
            <form method="POST" enctype="multipart/form-data">
                <h2 align="center">MyPage 수정</h2>

                    <!-- 프로필 이미지 영역 -->
                    {% if user.image_path %}
                    <img src="{{ url_for('static', filename=user.image_path)}}" alt="사용자프로필이미지"
                        class="rounded mx-auto d-block">
                    {% else %}
                    <img src="{{ url_for('static', filename='basic_profile.png')}}" alt="기본프로필이미지"
                        class="rounded mx-auto d-block">
                    {% endif %}

                    <!-- 프로필 파일 수정 버튼 -->
                    <label for="imageFile" class="form-label">프로필 이미지</label>
                    <input name='imageFile' class="form-control" type="file" id="imageFile">

                    <!-- 기본 정보 영역 -->
                    <div class="mb-3">
                        <label for="InputEmail1" class="form-label">이메일</label>
                        <input name="email" type="email" class="form-control" id="InputEmail1"
                            aria-describedby="emailHelp" placeholder="{{ user.email }}">
                    </div>

                    <div class="mb-3">
                        <label for="Nickname1" class="form-label">닉네임</label>
                        <input name="nickname" type="text" class="form-control" id="Nickname1"
                            placeholder="{{ user.nickname }}">
                    </div>

                <button type="submit" class="btn btn-primary">정보 수정 제출</button>
            </form>
        </div>
    </div>
</div>

{% endblock %}
```
- mypage.html 코드에서 다음이 변경
    - 삭제 : `fieldset`, `form:action` 
    - 변경 : `form:post`, 정보 수정으로 키워드 변경
    - 추가 : 이미지 전송을 위해서 form태그에 `enctype = "multipart/form-data"`를 추가
- 추가 : 이미지 파일 업로드 HTML
    - [ref. File input](https://getbootstrap.com/docs/5.2/forms/form-control/#file-input)
    - `<label for="imageFile" class="form-label">프로필 이미지</label>`
    - `<input name='imageFile' class="form-control" type="file" id="imageFile">`

### form 의 enctype?
- Form을 통해 데이터 전송시 인코딩 타입에 대한 명시를 해야합니다.
    - (기본값) application/x-www-form-urlcencoded
        - 파일이 없는 폼에 사용. multipart/form-data 를 제외한 모든 경우에 사용.
        - 모든 문자들은 서버로 보내기 전에 인코딩됨을 명시.
    - multipart/form-data
        - 모든 문자를 인코딩하지 않음을 명시.
        - 파일(<input type="file">)이 포함된 폼을 전송할 때. 즉, 파일을 서버로 전송할 때 사용.
    - text/plain
        - 인코딩 없이 전송. 보안성이 없어 디버깅 용도로만 사용. 잘 안쓰인다.
        - 정확하겐 공백 문자(space)는 '+'로 변환, 나머지 문자는 모두 인코딩 안되었음을 명시.


## 파일 저장을 위한 View 준비 - mypage_views.py
- [ref. Flask > Uploading File](https://flask.palletsprojects.com/en/2.1.x/patterns/fileuploads/)
    - werkzeug는 자동으로 설치되어있다.(Flask 의존성)

### 파일 업로드 처리를 위한 View 작성(이미지 반영) - mypage_views.py
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
    return render_template('mypage.html')


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
                    
                    return redirect(url_for('mypage_views.mypage'))
                else:
                    # 확장자가 허용되지 않음
                    flash('이미지 파일은 png jpg jepg gif 만 지원합니다.', category = "error")
                    return redirect(request.url)
        
    return render_template('mypage_update.html')

```
- 참조 : `from werkzeug.utils import secure_filename` ,  `import os`
- 허용 이미지 목록 : `ALLOWED_EXTENSIONS = ['png','jpg','jpeg','gif']`
- 허용 이미지 여부 확인 함수 : `def allowed_file(filename):`
- 첨부된 이미지가 있는지 확인 : `if image_file.filename:`
    - 디버그 모드를 보면 requests.files가 있다.
        - 내부에 input에 name을 준 'imageFile`이 있다.
- 허용된 이미지인지 확인 : `if allowed_file(image_file.filename):`
- 첨부된 파일 이름, 파일 타입, 저장할 이미지 주소를 저장한다.
    - 참고 예제처럼 flask app을 가져올 수 없으니 다른 방법으로 경로 계산
    - `./website/static` 을 하거나 `f'{os.path.dirname(__file__)}/static'`
    - 파일 확장자(filetype)은 `def allowed_file(filename):`의 방식을 참고
        - 해당 함수는 `rsplit()`을 사용하여 확장자를 분리시켜 검사중
- 파일 저장시에는 user.id가 들어가도록
    - 다른 유저가 같은 이미지 파일명으로 올릴 수도 있으니까.
    - `image_file.save(f'{image_path}{current_user.id}.{filetype}')`
- 저장 후엔 DB에 반영
    - 탐색 : `user = User.query.get(current_user.id)`
    - 반영 : `user.image_path = f'{current_user.id}.{filetype}'`