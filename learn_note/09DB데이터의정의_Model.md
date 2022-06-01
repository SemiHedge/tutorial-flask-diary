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
    - title, content, datetime


## User 모델 정의 - models.py
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
- User 모델 데이터 속성 정의 
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
         

## Note 모델 정의 - models.py
- User모델을 참조하여 Note 모델도 정의

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


# define Note Model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(2000))
    datetime = db.Column(db.DateTime(timezone=True), default=func.now())
```
- Note 모델 데이터 속성 정의
    - id : Integer, 메모장의 고유번호(id). 기본키(primary_key)
    - title : String, 메모의 제목
    - content : String, 메모장 내용, 글자 제한을 두지 않는다면 데이터 타입을 Text로 고려
    - datetime : DateTime, 작성 시간. 이를 위해 DB가 타임 스탬프를 자체 계산하여 지시할 수 있도록 함수를 참조할 필요가 있었습니다.
        - 때문에 `from sqlalchemy.sql import func`을 참조하고
        - SQL에서 현재 시간 함수인 now()를 실행하도록 `func.now()`를 작성

### 현재 시간 작성 datetime.utcnow vs func.now()
- 파이썬으로 DB에 현재 시간을 작성한다면? 생각해볼 수 있는 것
    - `from datetime import datetime`을 통한 `datetime.utcnow`
        - [ref. flask-sqlalchemy > Simple Relationships](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#simple-relationships)
    - `from sqlalchemy.sql import func`를 통한 `func.now()` 또는 ` func.current_timestamp()` (두 개는 사실 같은 함수)
- `flask-sqlalchemy` 문서 내용이라 전자가 맞는 것 같은데, 후자를 권장함.
    - 이유 : [ref. StackOverflow > SQLAlchemy default DateTime](https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime)
        - "'데이터가 저장된 시각'이라는 측면에서는 웹 서버 애플리케이션(또는 앱)의 시간이 아닌 DB에 저장된 시간이 기록되어야 함"
        - "클라이언트 시간으로 기록하기에는 네트워크 지원 등의 이유로 실제 DB에 저장된 시각과 차이가 있을 수 있음"
        - 모든 데이터는 DB기준으로 기록되어야함.
            - 예시 상황 : 한정판 티켓팅을 생각해보자. 사용자가 보는 화면을 기준으로 결과를 처리하고 이후에야 DB에 반영을 하면... DB 재고가 없는데도 구매 처리가 되버려서 -값을 가질 수도 있다. DB를 타고가는 건 DB입장을 우선적으로 생각하자.
- [ref. SQLAlchemy > SQL and Generic Functions](https://docs.sqlalchemy.org/en/14/core/functions.html)
    - "sqlalchemy.sql 함수는 데이터베이스별로 갖고있는 렌더링, 반환 유형 및 인수 동작 등을 활용할 수 있도록 합니다. `func` 속성을 사용하여 SQL이라면 일반적(공통적)으로 갖고있는 함수들을 호출(실행)시킵니다."