# DB에 관리되는 데이터를 클래스로 정의해보자.
- django의 Model를 경험해보았다면 좋습니다.
- 파이썬 class 선언 문법을 알아야 합니다.
- 파이썬 Mixin(믹스인)을 통한 다중상속 개념을 찾아보고 오면 좋습니다.

## Database Model 정의 - models.py
-  유저(User)와 메모장(Note)에 대한 데이터를 정의할 예정

```python
from . import db  # from website import db

# define User Model
class User(db.Model):
    pass


# define Note Model
class Note(db.Model):
    pass
```
- `__init__.py`에 선언한 db를 가져옵니다.
    - `__init__.py`를 통해 website폴더를 패키지화 했습니다.
    - `from . `을 하면 현재 속한 패키지에 선언된 값, 함수를 가져올 수 있고
    - 현재 패키지 명이 website라 `from website`와 동일한 의미입니다.
- 데이터베이스에 저장될 데이터에 대하여 class를 선언해줍니다.

## 각 데이터 모델에 필요한 속성(DB에서는 column)의 정의
- User
    - id : 유저 데이터를 구분하기위한 유일 값. 기본키(primary_key)
    - email, password, nickname
- Note
    - id : 메모 데이터를 구분하기위한 유일 값. 기본키(primary_key)
    - content, datetime


## User 모델 정의
```python
from . import db  # from website import db
from flask_login import UserMixin


# define User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nickname = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200))


# define Note Model
class Note(db.Model):
    pass
```
- `flask_login`의 `UserMixin`클래스를 상속시킵니다.
    - [ref. Flask-Login](https://flask-login.readthedocs.io/en/latest/)
        - "Flask-Login은 Flask에 대한 사용자 세션 관리를 제공합니다. 로그인, 로그아웃 및 장기간에 걸친 사용자 세션 기억과 같은 일반적인 작업을 처리합니다."
        - "다음 작업을 수행합니다."
            - "세션에 활성 사용자의 ID를 저장하고 쉽게 로그인 및 로그아웃할 수 있다."
            - "로그인한(또는 로그아웃한) 사용자의 보기(Views) 제한."
            - "일반적으로 까다로운 '기억(remember me)' 기능을 처리합니다."
            - "쿠키(Cookie) 도둑이 사용자의 세션(Session)을 도난하지 않도록 보호"
            - "나중에 Flask-Principal 또는 기타 인증 확장과 통합할 수 있다."
    - [ref. Flask-Login > UserMixin](https://flask-login.readthedocs.io/en/latest/#user-object-helpers)
        - "이것은 Flask-Login이 사용자 개체가 가질 것으로 기대하는 메서드에 대한 기본 구현을 제공합니다."
- User 모델의 속성은 flask-sqlalchemy 예제를 참고했습니다.
    - [ref. flask-sqlalchemy > A Minimal Application](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application)
- 모델의 데이터 속성 정의 
    - `db.Column()`로 선언하고, 이에 알맞는 데이터 타입, 키설정, Null가능여부 등을 해준다.
        - id : Integer, primary_key
        - email : String, unique_key
        - password : String
        - nickname : String, unique_key

## Flask-SQLAlchemy의 모델 선언 시 데이터 타입 - db.Column()
- [ref. Declaring Models](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/)
- `Integer, String(size), Text, DateTime, Float, Boolean, PickleType, LargeBinary`

## 좀 더 알아보자. SQLAlchemy의 Column()
- [ref. sqlalchemy.schema.Column](https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column)
- 파라미터(parameters) 영역을 확인
    - 첫번째 인자 `name` : 생략가능, 데이터베이스에서의 컬럼 명
    - 두번째 인자 `type` : 데이터 타입
    - optional 인자들(*args)
        - `autoincrement` : Integer일 때 자동 증가여부
        - `nullable` : NULL 값의 허용 여부
        - `primary_key` : 기본키로 설정 여부
        - `unique` : 유일키로 설정 여부
        - 그 외 등등
         
