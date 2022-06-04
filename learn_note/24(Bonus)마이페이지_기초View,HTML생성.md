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
    return render_template('mypage.html', user=current_user)


# 나의 정보 수정 페이지
@mypage_views.route('/mypage/update', methods=['GET','POST'])
@login_required
def mypage_update():
    return render_template('mypage_update.html', user=current_user)
```
- blueprint 이름 : `mypage_views`
- route : `/mypage`, `/mypage/update`
- 둘 다 로그인 필수 페이지이니 
    - `@login_required`
    - `render_template(..., user=current_user)`

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
        return User.query.get(int(id))  # primary_key

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



- [ref. Flask > Uploading File](https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/)