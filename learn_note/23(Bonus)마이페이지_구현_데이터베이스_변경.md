## 완성된 프로그램에 추가 기능 붙이기(파일첨부, 사진추가)
- 추가 기능을 넣는다는 건 쉽지않다.
    - 과거의 나를 후회하는 순간
- 초기 설계에 '확장성'을 신경. 신중하게 됨
    - 그렇다고 초기 프로그램 설계에 너무 시간을 많이 쏟으면 안됨

## 나의 정보 페이지(마이페이지)를 구현한다면 무슨 기능을 지원하게 될까? (리스트업)
- 프로필 사진 보기
- 프로필 사진 등록/변경
- 닉네임 변경
- 패스워드 변경
- 회원 탈퇴

## 기존 프로젝트에 추가 또는 변경해야 될 부분은?
- 나의 정보 조회 페이지 : mypage.html
- 나의 정보 수정 페이지 : update_mypage.html
- 나의 정보 관련 기능을 처리할 : mypage_views.py
    - 기존 views.py파일에서 처리해도 되지만..
    - 기존 views.py는 메모 관련 기능이 대부분이라 성격이 note_views.py 같다.
    - 새로운 기능 추가이니 분리시켜 작업하자
- DB.user 테이블에 사진 리소스 경로 추가
    - Models.py에 새로 user테이블을 정의하고
        - 기존 DB를 날리고 새로 DB를 생성하거나
        - 새로운 db를 반영하기위한 명령어 `flask db upgrade`를 입력하거나
        - SQL 문으로 직접 새 컬럼을 추가하여, 기존 DB를 보존하거나

## 사진은 서버의 데이터베이스에서 어떻게 저장할까?
- 먼저 '데이터베이스는 주로 어떤 데이터 유형을 저장하는가?'를 알아야합니다.
- 데이터 베이스는 정형 데이터를 저장하는데 수월합니다.
    - [ref. 정형, 비정형, 반정형 데이터](https://chankim.tistory.com/3)
- 이미지는 비정형이라 데이터베이스에 저장하는 건 비효율적입니다.
    - 저장은 할 수는 있겠으나, 성능면에서 많이 깎아집니다.
        - [ref. Is it better to store images in a database or a file system?](https://www.quora.com/Is-it-better-to-store-images-in-a-database-or-a-file-system)
        - [ref. Storing images in Blob vs File System](https://medium.com/@anilsingh.jsr/storing-images-in-blob-vs-file-system-3d704988e44e)
- 이미지는 파일로서 폴더(또는 파일서버)에 저장하고, 데이터베이스는 이미지 파일 주소(텍스트)를 저장합니다.

## 데이터 모델 재정의 - models.py
```python
from . import db  # from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# define User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nickname = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200))
    notes = db.relationship('Note')
    image_path = db.Column(db.String(255), unique=True, nullable=True)


# define Note Model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(2000))
    datetime = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))    
```
- 추가 : `image_path = db.Column(db.String(255), unique=True, nullable=True)`

## 새로운 db 반영 - flask db upgrade
- 기존 database.db를 삭제해도 됩니다. 그럼 `__init__.py > create_database()`가 실행되면서 새로운 db를 생성해줍니다.
- 하지만 기존 Database 정보를 살리려면 
    - 새로운 db를 적용하기위해 `flask db upgrade`를 하거나
    - 직접 DB에 접근하여 수정하기위해 SQL문을 작성해야합니다.

## Flask DB를 관리를 해주는 Flask-Migrate 설치
- [ref. Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
- Flask 데이터베이스를 마이그레이션(migration)을 지원한다
    - 마이그레이션? : DB 이관, 이주, 변경, 통합 등
- 설치 : `pip install Flask-Migrate sqlalchemy`


### Flask-Migrate 적용 - __init__.py
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy import MetaData

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'semicircle_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # 블루프린트 인스턴스 가져오기
    from .views import views
    from .auth import auth

    # 플라스크 앱에 등록하기
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

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


# 데이터 베이스 생성 함수
def create_database(app):
    # db파일이 확인안될 때만 생성
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('>>> Create DB')
```
- 라이브러리 참조
    - `from flask_migrate import Migrate`
    - `from sqlalchemy import MetaData`
- Flask-Migrate 적용
    - [ref. ](https://flask-migrate.readthedocs.io/en/latest/#installation)
        - `migrate = Migrate(app, db)`
        - 그런데 이것만 참고하여 적용하면 에러가 남.
    - [ref. ](https://stackoverflow.com/questions/62640576/flask-migrate-valueerror-constraint-must-have-a-name)
        - 추가 : 변수 `convention`, `metadata` 생성
        - 변경 : `db = SQLAlchemy(metadata=metadata)` , `migrate = Migrate(app, db, render_as_batch=True)`
            - 위의 레퍼런스에는 app추가하라고 하지만, 현재 우리의 Flask app은 함수 `create_app`에서 만들어지니 동일하게 적용하기에는 애매하다.
            - [ref. FlaskSQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/) 를 보면 `app`, `metadata` 모두 None으로 옵션사항이고, 두번째 예제처럼 Flask APP이 함수 내부에서 생성되는 경우, `db.init(app)`에서 SQLAlchemy를 app에 적용할 수 있다.

### 새로운 models.py로 Database를 반영
- [ref. flask-migrate](https://flask-migrate.readthedocs.io/en/latest/#flask-migrate)
    - `flask db init`
        - migrations 폴더가 생성됨.
        - 만일 flask db 명령어를 다시 실행할 필요가 있다면 이 폴더를 지우고 다시 시작
    - `flask db migrate`
    - `flask db upgrade`

### (참고)만일 `Can't locate revision identified by 'OOOOOOOOOOOO'` 에러가 뜬다면?
- [ref. Can't locate revision identified by '30dc7f6b846a'](https://github.com/prerit2010/Result-aggregation-server/issues/37)
    - 에러에 뜬 `OOOOOOOOOOOO`를 참고하여
        - `flask db revision --rev-id 30dc7f6b846a`
        - `flask db migrate`
        - `flask db upgrade`

### Database 확인
- user 테이블에 image_path가 추가되었는지 확인
