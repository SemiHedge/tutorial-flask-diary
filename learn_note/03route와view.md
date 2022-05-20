# 웹 사이트 페이지와 이에 대한 url을 정의해보자.
- 파이썬의 데코레이터(decorator) 문법을 알아두면 좋습니다.
- HTML의 태그 h1, p 를 알아두면 좋습니다.
- 대문 페이지와 계정관련 페이지로 향하는 URL을 구현.


## Blueprint 생성 - views.py 
```python
from flask import Blueprint

views = Blueprint('views', __name__)
```
- `flask.Blueprint`를 가져옵니다.
- `Blueprint`를 이용하면 플라스크 APP의 모든 url을 한 곳에서 관리하지 않아도 됩니다.
    - 여러 파일에서 url에 대한 정의를 선언할 수 해준다.
    - 즉, 이곳저곳에 뿌려진 url의 정의를 수집하여 한 곳으로 모아준다.
    - 관련해서는 url을 한 곳에 구현했던 영상을 구경하러 가보자.
- `views.py`에서 사용할 `Blueprint`는 편하게 views라고 합니다.

### Blueprint 자세히 보기
- [ref. Blueprint Object](https://flask.palletsprojects.com/en/2.1.x/api/?highlight=blueprint#flask.Blueprint)
- 매개변수들
    1. `name` : required. Blueprint의 이름 정의
    2. `import_name` : required. Blueprint의 패키지 이름. 일반적으로 `__name__` 입력


### Blueprint를 이용한 라우트(Route) 정의 - views.py
- 뷰를 정의하여 보여질 페이지와 경로를 정의합니다.
- '클라이언트 요청 > 서버의 응답'을 과정을 세부적이게 구현할 필요가 없다.
    - 이는 데코레이터로 `Blueprint.route`가 해줄 예정
    - 우리는 동작하기위해 필요한 정보만 입력하면 된다.

```python
from flask import Blueprint

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return '<h1>home</h1>'
```
- url의 끝부분(end-point)를 인자로 입력
- 클라이언트 요청에 응답할 데이터를 return시키는 함수를 생성합니다.
    - 함수 이름은 동작에 영향을 끼치진 않지만, 코드관리를 위해 의미있는 것을 입력합시다.


### views.py의 Blueprint를 Flask App에 등록 - __init__.py
- 다른 곳에서 생성된 Blueprint를 `__init__.py`에 등록.
    - Flask APP에 관리되는 Blueprint가 있다는 것을 알리기 위함.


```python
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'semicircle_secret_key'

    # 블루프린트 인스턴스 가져오기
    from .views import views

    # 플라스크 앱에 등록하기
    app.register_blueprint(views, url_prefix='/')

    return app
```
- `url_prefix` : url접두사. 해당 블루프린트를 이용할 때 기본적으로 붙을 url을 적습니다.
    - 현재는 딱히 구분할 필요가 없기에 모두 `/` 문자열로 입력합니다.


## Flask App 실행 - main.py
- Not Found가 아닌 home 문자열이 나오는 페이지가 나온다.
    - return했던 `<h1>home</h1>`이 렌더링해서 받아졌다.
- 일어난 일의 순서를 나열해보자.
    1. 웹 브라우저에서 url 접속을 함
    2. Flask 서버에 클라이언트 요청이 전달
    3. Flask APP에서 일치하는 url을 탐색
    4. Blueprint 'views'를 이용하여 Flask APP의 라우팅 시스템(Routing System)에 url을 등록해놨음
        - Route는 외부에서 웹 서버로 접근 시 사용한 url을 확인하여 매핑된 함수를 실행하고, 그 결과를 돌려주는 역할을 한다.
    5. 따라서 `views.py`의 `home`함수가 실행되고
    6. 그 return값인 `<h1>home</h1>`를 받고
    7. 이 값을 렌더링하여 클라이언트에게 응답한다.


## Blueprint 생성 - auth.py
- `views.py` 에서 작성한 코드를 복붙해서 조금만 수정
    - Blueprint를 저장할 변수, 이름만 변경
```python
from flask import Blueprint

auth = Blueprint('auth', __name__)
```

### auth.py의 Blueprint를 Flask App에 등록 - __init__.py
- 다른 곳에서 생성된 Blueprint를 `__init__.py`에 등록.
    - Flask APP에 관리되는 Blueprint가 있다는 것을 알리기 위함.

```python
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'semicircle_secret_key'

    # 블루프린트 인스턴스 가져오기
    from .views import views
    from .auth import auth

    # 플라스크 앱에 등록하기
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
```

### Blueprint를 이용한 라우트(Route) 정의 - auth.py
- 로그인, 로그아웃, 회원가입 페이지의 url을 정의해보자.
- route 함수에 추가적인 url을 작성하여 분기를 만들어준다.
    - `login`,`logout`,`register`을 해도되나
    - Github을 포함하여 외국의 경우 `Sign-in`, `Sign-Out`, `Sign-Up`이 요새 자주보이니 이를 반영해보자.

```python
from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/sign-in')
def sign_in():
    return "<p>Sign-In</p>"

@auth.route('/sign-out')
def sign_out():
    return "<p>Sign-Out</p>"

@auth.route('/sign-up')
def sign_up():
    return "<p>Sign-Up</p>"
```

## Flask App 실행 - main.py
- 각 페이지가 잘 나오는 지 확인해보자.
    - http://127.0.0.1:5000/sign-in
    - http://127.0.0.1:5000/sign-out
    - http://127.0.0.1:5000/sign-up


### 짚고가기 - Blueprint
- Blueprint는 이곳 저곳에 떨어져있는 URL과 함수의 매핑. 즉 route 등록을 한 곳에 모아 정리하고 활용되게 도와준다.

### ref. 좀 더 알아보자
- [ref. URL Route Registrations](https://flask.palletsprojects.com/en/2.1.x/api/?highlight=route#url-route-registrations)
    - Flask의 Routing System에 등록하는 방법을 소개합니다.
- [ref. flask.Flask.route](https://flask.palletsprojects.com/en/2.1.x/api/?highlight=route#flask.Flask.route)
    - 가장 기본이 되는 url 등록 함수입니다.
    - 다만 코드관리를 하기 위해 Blueprint를 활용하고 있습니다.
    - `Blueprint.route`는 `Flask.route`를 다른 곳에서 쓸 수 있게 한 것일 뿐입니다.
- [ref. flask.Blueprint.route ](https://flask.palletsprojects.com/en/2.1.x/api/?highlight=route#flask.Blueprint.route)