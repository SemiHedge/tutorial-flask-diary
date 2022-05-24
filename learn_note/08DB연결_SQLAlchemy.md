# Database를 활용하기위한 Flask-SQLAlchemy

## 초기 DB 생성 - __init__.py
- Flask가 DB와 통신하기위한 객체를 생성해야합니다.
- 데이터베이스가 없으니 생성하도록 합시다.
- DB유형은 간단하게 sqlite3를 사용합니다.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
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

    return app
```
- `SQLAlchemy` 클래스를 참조합니다.
- 변수 db를 선언하고 SQLAlchemy 객체(인스턴스)를 생성합니다.
    - SQLAlchemy 객체는 DB와 정보를 주고 받을 예정
    - SQLAlchemy는 DB를 가리키고 있기 때문에
    - 사실상 때문에 파이썬 입장에서는 db라고 봐도 무방하겠죠?
    - [ref. flask-SQLAlchemy > API](https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#configuration)
        - "이 클래스는 하나 이상의 Flask 애플리케이션에 대한 SQLAlchemy 통합을 제어하는 ​​데 사용됩니다. 객체를 초기화하는 방법에 따라 즉시 사용할 수 있거나 필요에 따라 Flask 애플리케이션에 첨부됩니다."
    - db cursor라고도 볼 수 있겠다. 이를 통해 DB에 CRUD 작업을 수행한다.   
- flask 앱 실행되면서 db와 소통을 합니다. 실제 DB의 위치를 설정해줍니다. 
    - [ref. flask-SQLAlchemy > Quickstart](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#quickstart)
    - 슬래시(/)를 세 번 합니다.
- 생성한 SQLAlchemy 인스턴스에 사용할 flask App을 넣어 초기화 시킵니다.
    - `flask-SQLAlchemy`문서에는 SQLAlchemy 객체 생성시에 인자로 넣지만, 현재 코드구조상 그러질 않으니까. 이렇게 초기화.


