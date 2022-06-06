## base.html에 mypage 메뉴
- 로그인할 때만 보이도록 하자

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
                    {% if user.is_authenticated %}
                    <!-- 로그인 되었을 때 -->
                    <li class="nav-item">
                        <a href="/" class="nav-link">Home</a>
                    </li>
                    <li class="nav-item">
                        <a href="/sign-out" class="nav-link">Sign Out</a>
                    </li>
                    <li class="nav-item">
                        <a href="/mypage" class="nav-link">My Page</a>
                    </li>
                    {% else %}
                    <!-- 로그인 안되었을 때 -->
                    <li class="nav-item">
                        <a href="/sign-in" class="nav-link">Sign In</a>
                    </li>
                    <li class="nav-item">
                        <a href="/sign-up" class="nav-link">Sign Up</a>
                    </li>
                    {% endif %}
                </ul>
        </div>
    </nav>
    
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

## Pythonanywhere에 재배포
- github에 프로젝트를 관리하고 있다고 가정
- 로컬 PC의 라이브러리 정보를 저장한다.
    - `pip3 freeze > requirements.txt`
- Github에 현재 상황을 `PUSH`한다.
- Pythonanywhere의 Console에서 
    - `git pull` : 최신 코드로 가져오고
    - `pip3 install -r requiremnets.txt` 로 라이브러리 설치
        - `Flask-Migrate` 등을 설치했으므로
    - `export FLASK_APP=main.py` , `flask db upgrade` 로 db 새로 반영
        - `migrations`폴더도 같이 올렸으므로
        - 만일 에러가 난다면 그래도 확인해보고, 적용이 안되었다면 다시 생성하자
            - `migrations` 폴더 삭제
            - `flask db init`, `flask db migrate`, `flask db upgrade`

## (주의) 이미 유저가 확보된 서비스라면 DB 백업본을 미리 만들거나 다운받아두자
- Github에 올릴 때 DB파일은 빼는 게 보통
    - 로컬 PC는 임시 데이터, 실제 돌아가는 서비스와는 별개의 DB
- 기존 서비스에 돌아가는 곳에 DB를 덮어버린다면? > 유저 정보 증발
- 업로드 파일에서 제거하는 방법 `.gitignore`
    - db파일 제외하도록 맨 위에 추가해두자
```
# database file
*.db
```

### 만일 .gitignore에 적용했으나 제외가 안된다면?
- 이미 한번 commit&push된 파일은 계속 반영된다. (캐시문제)
    - [ref. gitignore가 적용되지 않을 때](https://sunnytdy.tistory.com/8)
```
git rm -r --cached .
git add .
git commit -m "clear git cache"
```