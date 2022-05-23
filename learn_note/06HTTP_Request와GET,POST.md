# 웹의 기본 지식 http requests, get, post

## HTTP : HyperText Transfer Protocol
- url을 입력하여 웹 사이트를 요청하고 응답받아 우리가 보는 그 과정은 '통신'
- '통신'에는 규약과 방식(도구)가 있어야 함 > 프로토콜
- 즉, 웹 브라우저를 통해서 주고받는 프로토콜 > HTTP

## HTTP를 통해서 우리가 하는 일 - Method
- 대부분은 프로그램은 CRUD의 일을 처리합니다.
    - Create : 데이터의 생산
    - Read : 데이터의 조회
    - Update : 데이터의 수정(업데이트)
    - Delete : 데이터의 삭제
- 이를 참고하여 대표적인 HTTP Method 4가지를 확인합니다.
    - GET : 웹 자원의 조회
    - POST : 웹 자원의 생성
    - PUT : 웹 자원의 수정(업데이트)
    - DELETE : 웹 자원의 삭제

### GET - 웹 사이트의 조회, 검색 등
- 기본적인 웹 페이지의 이용은 GET 통신을 주로 사용합니다.
- 데이터의 조회를 주된 목적으로 사용합니다.

### POST - 회원 가입, 블로그 글쓰기 등
- 통신 후 데이터가 남는 형태는 POST 통신을 주로 사용합니다.
- 데이터의 생산을 주된 복적으로 사용합니다.


## POST로 회원가입 구현 - auth.py
```python
from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    return render_template('sign_in.html')

@auth.route('/sign-out')
def sign_out():
    return render_template('sign_out.html')

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    return render_template('sign_up.html')
```
-`route`에 `GET`,`POST` method로 통신됨을 추가합니다.
- 나중에 'GET', 'POST' 인가에 따라서 분기를 줄 예정
    - 회원가입 페이지에 접속했다 -> GET 통신
    - 제출을 눌러 회원가입 신청을 했다 -> form:POST -> POST 통신

### request로 POST로 요청된 값 확인 - auth.py
```python
from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)

@auth.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    return render_template('sign_in.html')

@auth.route('/sign-out')
def sign_out():
    return render_template('sign_out.html')

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # 데이터 확인
    data = request.form
    print(data)
    return render_template('sign_up.html')
```
- `request` 를 참조.
    - 클라이언트 요청에 대한 데이터가 담겨있습니다.
- `data = request.form` 로 form으로 입력한 데이터를 출력해봅시다.
    - GET으로 요청할 땐 안나오고
    - POST로 요청할 때만 값이 나온다.

```
ImmutableMultiDict([('email', 'semi@gmail.com'), ('nickname', 'Hedge'), ('password1', 'asdf'), ('password2', 'asdf'), ('checked', 'on')])
```

### POST 분기 생성 - auth.py
```python
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # form - input의 name 속성을 기준으로 가져오기
        email = request.form.get('email')
        nickname = request.form.get('nickname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 유효성 검사
        if len(email) < 5 :
            pass
        elif len(nickname) < 2:
            pass
        elif password1 != password2 :
            pass
        elif len(password1) < 7:
            pass
        else:
            pass  # Create User -> DB


    return render_template('sign_up.html')
```
- `request.method`의 값을 확인한다.
- `form`태그 내부의 `input`들의 `name`의 값을 가져온다.
- '이메일이 맞나?' 싶은 검사. 즉, 이메일에 대한 유효성 검사를 한다.
- 나머지 코드는 일단 유지
