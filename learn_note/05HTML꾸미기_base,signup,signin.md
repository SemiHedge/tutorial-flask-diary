# 본격 기능 개발전 HTML 꾸미기
- html, css, js를 알아두면 좋습니다.
- bootstrap.js를 사용할 예정입니다.
- 본격적인 백엔드 작업 전 템플릿 기초를 잡아둡시다.

## 여기 부분은 따라하기 식 위주로 갑니다.
- HTML, CSS, JS 강의가 아니라는 점.
- 빠른 디자인 꾸미기를 위해서 Bootstrap.js를 사용
- 실무에선 주로 프론트엔드 개발자가 담당합니다.
- 그래도 백엔드 개발자도 최소한의 지식은 있어야합니다.

## 부트스트랩?
- CSS 프레임워크
- 디자인 관련하여 폼과 기능들을 제공합니다.

## 부트스트랩 가져오기 - base.html
- 모든 곳에 bootstrap.js를 가져오려면 base.html에 정의하면 됩니다.
- 현재의 최신 버전인 bootstrap 5.2.0을 쓰겠습니다.
- [ref. Bootstrap 5.2.0 - Quick start](https://getbootstrap.com/docs/5.2/getting-started/introduction/#quick-start)
- 이전에 학습을 위해 사용된 `block:description` 코드는 삭제했습니다.


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

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2" crossorigin="anonymous"></script>
</body>
</html>
```

## Flask 정적 파일용 폴더(static) 불러오기
- 웹페이지는 사진, 동영상 등의 미디어 파일도 존재한다.
- 또한 CSS, JS 파일도 필요하기도 하다.
- 만일 `static/index.js`를 가져온다면
    - `<script src="{{ url_for('static', filename='index.js')}}"></script>`
    - `</body>` 바로 위에 작성하자.

## 페이지 꾸미기 Navbar - base.html
- Navbar 생성
    - [ref. Navbar > Nav](https://getbootstrap.com/docs/5.2/components/navbar/#nav)

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

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2" crossorigin="anonymous"></script>
    <script src="{{ url_for('static', filename='index.js')}}"></script>
</body>
</html>
```



## 페이지 꾸미기 Container- base.html
- container는 부트스트랩에서 내용(콘텐츠)를 담을 때 사용하는 레이아웃 용 기본 블록입니다.
    - [ref. Container](https://getbootstrap.com/docs/5.2/layout/containers/)

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

## 페이지 꾸미기 - home.html
- `block:content`를 채워줍니다.

```html
{% extends "base.html" %}

{% block title %}Title - Home{% endblock %}

{% block content %}
<h1>Welcome to Homepage!</h1>
{% endblock %}
```

## 페이지 꾸미기 - sign_up.html
- bootstrap form태그 가이드를 활용해보자
    - [ref. Form > Overview](https://getbootstrap.com/docs/5.2/forms/overview/#overview)
- 해당 페이지가 SignUp 페이지임을 `h2`로 표기
- 이메일, 닉네임, 비밀번호, 비밀번호 확인, 검토 여부에 대한 입력을 만듭시다.
    - 이를 입력받는 input에 `name` 속성을 추가해줍니다.
        - 이는 서버에서 값 확인 시 사용됩니다.

```html
<!-- sign_up.html -->
{% extends "base.html" %}
{% block title %}Title - SignUp{% endblock %}

{% block content %}
<form method="POST">
    <h2 align="center">Sign Up</h2>
    <div class="mb-3">
      <label for="InputEmail1" class="form-label">가입할 이메일</label>
      <input name="email" type="email" class="form-control" id="InputEmail1" aria-describedby="emailHelp">
      <div id="emailHelp" class="form-text">가입할 이메일을 입력하세요</div>
    </div>

    <div class="mb-3">
        <label for="Nickname1" class="form-label">닉네임</label>
        <input name="nickname" type="text" class="form-control" id="Nickname1">
    </div>

    <div class="mb-3">
      <label for="InputPassword1" class="form-label">비밀번호</label>
      <input name="password1" type="password" class="form-control" id="InputPassword1"">
    </div>

    <div class="mb-3">
        <label for="InputPassword2" class="form-label">비밀번호 재확인</label>
        <input name="password2" type="password" class="form-control" id="InputPassword2"">
    </div>


    <div class="mb-3 form-check">
      <input name="checked" type="checkbox" class="form-check-input" id="Check1">
      <label class="form-check-label" for="Check1">위 내용을 확인했습니다.</label>
    </div>

    <button type="submit" class="btn btn-primary">제출</button>
  </form>
{% endblock %}
```

## 페이지 꾸미기 - sign_in.html
- 회원 가입에서 몇 개만 빼거나 수정하자.
    - `nickname`, `password2`, `checked`
    - `제출` -> `로그인`
- `sign_up.html`의 `block:content`영역을 복사해서 수정하자.

```html
<!-- sign_in.html -->
{% extends "base.html" %}

{% block title %}Title - SignIn{% endblock %}

{% block content %}
<form method="POST">
    <h2 align="center">Sign In</h2>
    <div class="mb-3">
      <label for="InputEmail1" class="form-label">이메일</label>
      <input name="email" type="email" class="form-control" id="InputEmail1">
    </div>

    <div class="mb-3">
      <label for="InputPassword1" class="form-label">비밀번호</label>
      <input name="password1" type="password" class="form-control" id="InputPassword1"">
    </div>

    <button type="submit" class="btn btn-primary">로그인</button>
  </form>
{% endblock %}
```