# 메세지 플래싱(MessageFlashing)?
- [ref. Flask-Message Flashing](https://flask-docs-kr.readthedocs.io/ko/latest/patterns/flashing.html#message-flashing)
- "플라스크는 플래싱 시스템을 가지고 사용자에게 피드백을 주는 정말 간단한 방법을 제공한다." 
- "플래싱 시스템은 기본적으로 요청의 끝에 메시지를 기록하고 그 다음 요청에서만 그 메시지에 접근할 수 있게 한다." 
- "보통은 플래싱을 처리하는 레이아웃 템플릿과 결함되어 사용된다."

## 그래서 flash가 뭔데?
- 서버에서 처리하며 생긴 오류사항/처리사항을 HTML에 넘겨줄 수 있는 기능
- 회원 가입시 이메일이 중복이라면?
    - `flash("중복된 이메일 주소입니다.")`
- 로그인 시 비밀번호가 틀렸다면?
    - `flash("비밀번호가 틀렸습니다.")`
- 추가적으로 flash의 category매개변수도 넣어줄 수 있습니다.
    - [ref. flask.flash](https://flask-docs-kr.readthedocs.io/ko/latest/ko/api.html#flask.flash)
    - `info` : `flash("공지로 등록 되었습니다.", category="info")`
    - `error` : `flash("해당글 삭제에 실패하였습니다.", category="error")`
    - `warning` : `flash("더 이상 해당 내용에 접근할 수 없습니다.)`
    - 위 3가지를 권장하나, 인자로 들어갈 문자열을 제한하진 않는다. 즉 이런 것도 가능하다.
        - `info` : `flash("한정판 티켓 신청에 성공하였습니다., category="success")`

## flash 적용하기 - auth.py
```python
from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    return render_template('sign_in.html')

@auth.route('/sign-out')
def sign_out():
    return render_template('sign_out.html')

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
            flash("이메일은 5자 이상입니다.", category="error")
        elif len(nickname) < 2:
            flash("닉네임은 2자 이상입니다.", category="error")
        elif password1 != password2 :
            flash("비밀번호와 비밀번호재입력이 서로 다릅니다.", category="error")
        elif len(password1) < 7:
            flash("비밀번호가 너무 짧습니다.", category="error")
        else:
            flash("회원가입 완료.", category="success")  # Create User -> DB

    
    return render_template('sign_up.html')
```
- `flash`를 참조합니다.
- 각 유효성검사에 맞는 message flash를 작성합니다.


## 메세지 플래싱 html 적용하기
- jinja 템플릿을 사용합니다.
    - 시작 : `{% with 변수명 = get_flashed_messages(with_categories=true) %}`
    - 끝 : `{% endwith %}`

### 회원가입 메세지 플래싱 적용하기 - base.html
- 플래싱 템플릿을 작성한다.
- 플래싱 메세지가 없는 경우에 대한 if를 작성한다.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">

    <title>{% block title %}Home{% endblock %}</title>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a href="/sign-in" class="nav-link">Sign In</a>
                    </li>
                    <li class="nav-item">
                        <a href="/sign-up" class="nav-link">Sign Up</a>
                    </li>
                    <li class="nav-item">
                        <a href="/sign-out" class="nav-link">Sign Out</a>
                    </li>
                    <li class="nav-item">
                        <a href="/" class="nav-link">Home</a>
                    </li>
                </ul>
        </div>
    </nav>
    
    <!-- Message Flashing -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for message in messages %}         
                <!-- error 메시지 -->
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <!-- content -->
    <div class="container">
        {% block content %}
        {% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2" crossorigin="anonymous"></script>
    <script src="{{ url_for('static', filename='index.js')}}"></script>
</body>
</html>
```
- `<!-- Message Flashing -->`를 확인하세요.
- 부트스트랩 5.2.0의 alert을 활용했습니다.
    - [ref. Bootstrap - Alerts](https://getbootstrap.com/docs/5.2/components/alerts/)
    - 부트스트랩은 클래스별로 디자인이 달라서 여러 상황에 맞게 다른 색깔을 제공할 수 있습니다.
    - primary, secondary, success, danger, warning, info, light, dark
- alert 닫기 버튼은 alert-Dismissing를 활용했습니다.
    - [ref. Bootstrap - Alerts#Dismissing](https://getbootstrap.com/docs/5.2/components/alerts/#dismissing)

### 실행 해보기
- 이메일을 너무 짧게 입력하면 메시지가 나온다.
    - `('error', '이메일은 5자 이상입니다.') [×]`

## flash 메세지 분리하기 + error|success 나누기
- `('error', '이메일은 5자 이상입니다.')`
    - `(category, message)` 로 분리하자
    - 파이썬의 for v in range(5)와 for i,v in range(5)처럼 작성
- `{% if %}`로 category의 분기(error|success)를 만들자.

```html
    <!-- Message Flashing -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                {% if category == "error" %}         
                <!-- error 메시지 -->
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                {% elif category == "success" %}
                <!-- success 메시지 -->
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                {% endif %}
            {% endfor %}
        {% endif %}
    {% endwith %}
```

### 실행해보기
- 이메일을 너무 짧게 입력하면 메시지가 나온다.
    - `이메일은 5자 이상입니다. [×]`
- 모든 값을 제대로 입력하면?
    - `회원가입 완료. [×]`
- 두 경우(error|success)에 따른 alert의 색 변화도 존재한다.