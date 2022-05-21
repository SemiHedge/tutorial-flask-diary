# URL을 만들었으니 제대로된 HTML을 만들기 시작.
- 기본적인 html 작성 및 파일 지식이 있으면 좋습니다.
- html, css, js의 관계를 알아두면 좋습니다.
    - 관련 영상을 참조하세요. https://www.youtube.com/watch?v=qom1GM2XI48

## HTML 파일의 저장소 - `templates` 폴더
- flask 프로젝트에서 사용될 HTML파일은 여기에 모아둔다.
- 그래서 해당 폴더를 'html 템플릿'이라고 부른다.

## 웹 페이지에서의 JS의 역할 
- 본래라면 프론트엔드에서 웹페이지를 구현할려면 최소 3가지를 알아야합니다.
    - HTML, CSS, JS
    - 이 중 JS만 프로그래밍 언어입니다.
- 웹 페이지에서의 JS 역할은 이런 것들이 있습니다.
    - 사용자마다 다른 페이지가 보이게 한다.
        - 로그인한 사람마다 다른 닉네임이 나오게 한다.
        - 로그인 한 사람 / 안한 사람이 다르게 나오게 한다.
    - 기능에 따라 다른 페이지가 보이게 한다.
        - 검색 페이지에서 '과자'와 '우동'을 각각 입력하면 형태는 같아도 서로 다른 검색결과가 나와야 한다.
    - 즉, 유동적인 페이지. 페이지의 동적화를 담당합니다.

## Jinja Template Language
- FLASK에서 Jinja Template Language라는 언어를 사용할 수 있습니다.
- 위 JS의 역할에서 설명한 '웹 페이지가 동적으로 반응해야 될 부분'을 JS가 아닌 Python코드와 유사한 방식으로 작성하여 그현할 수 있습니다.
- 그 외에도 여러 기능들을 제공합니다. 앞으로 알아봅시다.
    - 전체 웹사이트에 테마로 사용될 base.html을 만들거나
    - 데이터가 입력되었는지, 올바른 데이터인지 확인 등의 유효성 검사를 하거나
    - 그 외 기능들도 앞으로 알아봅시다.


## 템플릿 생성 - base.html
- 전체 웹 사이트의 테마가 될 base.html를 templates폴더 안에 생성합니다.
- html의 header, footer 등 어느 페이지에서도 유지되는 공통 부분을 구현합니다.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    
</body>
</html>
```

## Jinja - block 기능 - base.html
- 테마가 될 base.html에 채워질 지역을 정의해줍니다.
- 다른 페이지를 활용하여 채워지게될 빈칸을 만든다고 생각합시다.
- 다음과 같이 표기합니다. 만일 빈칸을 만들고 그 빈칸의 이름을 `title`이라고 정한다면
    - 빈 칸의 시작 : `{% block title %}`
    - 빈 칸의 끝 : `{% endtitle %}`
    - `{% block title %} 기본값 {% endtitle %}`
- 실습을 위해 title, description 두 개의 빈칸을 뚫어보겠습니다.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Default Title{% endblock %}</title>
</head>
<body>
    <h1>{% block description %}Defualt Description{% endblock %}</h1>
</body>
</html>
```

## 상세 템플릿 생성 - home.html
- 대문 페이지에 사용될 home.html을 생성.
- 먼저 기본 테마가 될 템플릿을 상속(extends)받습니다.
- 이후 빈 칸에 대한 내용을 작성해줍니다.

```html
{% extends "base.html" %}
{% block title %}Title - Home{% endblock %}
{% block description %}Description - Home{% endblock %}
```

### 렌더링 - views.py
- url접속시 위에 만들어진 템플릿. 즉, html들을 되돌려주도록 만듭니다.

```python
from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')
```
- `render_template`을 참조합니다.
    - 템플릿을 이용하여 클라이언트에게 보여질 전달될 결과물을 렌더링합니다.
- `render_template('home.html')`로 사용할 템플릿을 지정합니다.

### URL 접속해보기
- 대문페이지에 접속해봅시다.
    - 크롬 창 상단에 보이는 웹 페이지 이름도 바뀌고
    - 내부의 내용도 바뀌었고
    - 기본적인 형태는 base.html을 따르고 있습니다.
- 웹 브라우저에서 우클릭하여 페이지 소스 보기를 눌러 html 코드를 확인해봅시다.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Title - Home</title>
</head>
<body>
    <h1>Description - Home</h1>
</body>
</html>
```

### 상세 페이지 - sign-in, sign-out, sign-up 페이지
- `home.html`처럼 간단하게 페이지를 구현해놓는다. 

```html
<!-- sign_in.html -->
{% extends "base.html" %}
{% block title %}Title - SignIn{% endblock %}
{% block description %}Description - SignIn{% endblock %}
```

```html
<!-- sign_out.html -->
{% extends "base.html" %}
{% block title %}Title - SignOut{% endblock %}
{% block description %}Description - SignOut{% endblock %}
```

```html
<!-- sign_up.html -->
{% extends "base.html" %}
{% block title %}Title - SignUp{% endblock %}
{% block description %}Description - SignUp{% endblock %}
```

### 렌더링 - auth.py
- `render_template`함수 활용

```python
from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/sign-in')
def sign_in():
    return render_template('sign_in.html')

@auth.route('/sign-out')
def sign_out():
    return render_template('sign_out.html')

@auth.route('/sign-up')
def sign_up():
    return render_template('sign_up.html')
```