## Delete : 메모 삭제 기능 구현 - views.py, home.html
- 메모 삭제 버튼을 추가 필요
- DB에서 조회 -> 삭제하는 View가 필요
- ajax 를 적용해봅시다.
- 이미 JS를 안다면 좋습니다.

## ajax?
- 현재 페이지를 유지한체, 서버와 통신하는 기술
- 기본적인 요청 > 응답시 페이지의 변화
    - 어떤 요청을 서버에 하면
    - 서버가 기능을 수행하고 render_template이나 redirect
    - 페이지가 새로 렌더링 되몀 새로운 페이지로 이동됨
- ajax를 이용하면 현재 페이지를 유지한 체 서버와 통신을 하고 이후 JS를 통해 필요한 부분만 변경하는 기술도 구현할 수 있다.
    - 불필요하게 모든 페이지를 새로고침 하는 경우가 없어진다.
- 특정 영역 부분만 변경시키는 건 JS를 배워야하니, 혹시 백엔드에 관심이 있다면 최소한 ajax 통신을 구현하는 것까진 해보자.

## Delete : 삭제 버튼 추가
```html
{% extends "base.html" %}

{% block title %}
Title - Home
{% endblock %}

{% block content %}
<!-- 메모 생성 영역 -->
<form action="" method="post">
    <h2 align="center">Note</h2>
    <div class="form-floating">
        <input name="note-title" type="text" class="form-control" id="note-title" placeholder="name@example.com">
        <label for="note-title">Title</label>
    </div>
    <div class="form-floating">
        <textarea name="note-content" class="form-control" placeholder="Leave a content here" id="note-content"></textarea>
        <label for="note-content">Content</label>
    </div>
    <button type="submit" class="btn btn-primary">메모 저장</button>
</form>

<!-- 메모 조회 영역 -->
<div class="list-group">
    {% for note in current_user.notes %}
    <a href="#" class="list-group-item list-group-item-action">
        <div class="d-flex w-100 justify-content-between">
          <h5 class="mb-2">{{note.title}}</h5>
          <small class="text-muted">{{note.datetime}}</small>
        </div>
        <p class="mb-1">{{note.content}}</p>
        
        <!-- 메모 삭제 버튼 -->
        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
            <button class="btn btn-primary" type="button">수정</button>
            <button class="btn btn-primary" type="button">삭제</button>
        </div>
    </a>  
    {% endfor %}
</div>
{% endblock %}
```

- 삭제 버튼은 우측 정렬로 하는게 좋아보입니다.
    - [ref. Block buttons](https://getbootstrap.com/docs/5.2/components/buttons/#block-buttons)
- html 좀 공부하신 경우에 인라인 요소인 a태그에 블록요소 div태그를 넣는 게 이상할 수 있는데, html5에서는 a태그 안에 블럭요소가 들어옴을 허용합니다.
    -[ref. “Block-level” links in HTML5](http://html5doctor.com/block-level-links-in-html-5/)


### 버튼에 자바스크립트 함수 넣어두기 - home.html
- button 요소를 클릭했을 때 함수가 실행되도록 넣어둡시다. 
    - `onclick=deleteNote{{note.id}}`
    - JS 컨벤션에서 함수는 lowerCamerCase를 지향합니다.
        - [ref. 자바스크립트 스타일 가이드 - 네이밍 컨벤션 편](https://velog.io/@cada/%EC%9E%90%EB%B0%94%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8-%EC%8A%A4%ED%83%80%EC%9D%BC-%EA%B0%80%EC%9D%B4%EB%93%9C-%EB%84%A4%EC%9D%B4%EB%B0%8D-%EC%BB%A8%EB%B2%A4%EC%85%98-%ED%8E%B8)

```html
<!-- 메모 조회 영역 -->
<div class="list-group">
    {% for note in current_user.notes %}
    <a href="#" class="list-group-item list-group-item-action">
        <div class="d-flex w-100 justify-content-between">
          <h5 class="mb-2">{{note.title}}</h5>
          <small class="text-muted">{{note.datetime}}</small>
        </div>
        <p class="mb-1">{{note.content}}</p>
        
        <!-- 메모 삭제 버튼 -->
        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
            <button class="btn btn-primary" type="button">수정</button>
            <button class="btn btn-primary" type="button" onclick="deleteNote({{note.id}})">삭제</button>
        </div>
    </a>  
    {% endfor %}
</div>
```

## 자바스크립트 함수 작성법 - index.js
- JS에서 함수를 만드는 방법은 크게 두 가지 입니다.
    - [ref. ES6 - Function](https://www.tutorialspoint.com/es6/es6_functions.htm)
- 둘 중 아무거나 해도 되지만, 저는 익명함수 방법으로 진행하겠습니다.
```js
// 기본적인 함수 생성 방법
function deleteNote(x){
    console.log(x);
}
```

```js
// ES6 부터 자주 사용되는 익명 함수 생성 방법
const deleteNote = function(x){ console.log(x) }
```

## ajax 구현을 위해 Fetch() API 사용법 - index.js
- ajax는 json 데이터를 주고 받습니다.
- fetch api이 과정을 수월하게 해줍니다.
    - `fetch()` : ajax 요청
    - `.then()` : 그 이후의 액션
    - 주로 fetch().then() 로 작성되며 .then()은 추가적으로 붙일 수 있습니다.
    - [ref. Fetch 사용하기](https://developer.mozilla.org/ko/docs/Web/API/Fetch_API/Using_Fetch)
- `fetch()`는 `Promise객체`를 반환합니다.
    - [ref. Fetch API](https://developer.mozilla.org/ko/docs/Web/API/Fetch_API)
- 사용 예제

```js
fetch('http://example.com/movies.json')
  .then((response) => response.json())
  .then((data) => console.log(data));
```

### Delete: 서버에 요청을 보내는 ajax 작성 - index.js
```js
const deleteNote = function (noteId){
    console.log(`삭제할 메모 id ${noteId}`);

    // 전달할 데이터 정보(메모 정보)
    let note = {
        noteId : noteId
    }

    // 삭제 ajax
    fetch('/delete-note',{
        method : 'POST',
        body : JSON.stringify(note),
        headers: {
            "Content-Type": "application/json"
        },
    }).then((response) => response.json())
    .then(()=>{
        window.location.href = '/'; // 새로고침
    });
}
```
- fetch로 요청
    - 요청할 url
    - HTTP method, 전달할 값 body
    - 요청할 url은 언더스코어(_)가 아닌 하이픈(-)을 넣자.
        - [ref. REST API URI 규칙](https://velog.io/@pjh612/REST-API-URI-%EA%B7%9C%EC%B9%99)
- 첫번째 .then()
    - http는 기본적으로 문자열 통신이기 때문에
    - ajax 통신이 완료되면 보통 받은 값을 문자열 -> json형으로 변환한다.
    - 받은 값을 활용하진 않기에 필요없는 .then이나 통상적으로 넣어준다.
- 두번째 .then()
    - 삭제 로직이 이루어졌으니 전체 새로고침을 하자.
        - 현재는 특정부분만 삭제가 아닌 전체 새로고침으로 구현.
- `headers`에 `"Content-Type": "application/json"`를 넣어줍니다.
    - 전달되는 데이터 타입(mimetype) `application/json`임을 표시합니다.
        - 이것을 안하면 우리가 파이썬에서 사용할 `request.get_json()`이 `None`이 뜹니다.
        - 이를 표시안하고도 구현할 순 있긴 합니다(`import json`, `json.load(request)`) 그러나 flask에서 지원하는 기능이 있다면 가능한 이를 지향합시다.
- 아직 삭제 요청 url에 매핑되는 view는 구현하지 않았다.

### Delete : 메모 삭제 뷰(View) 구현 - views.py
```python
from flask import Blueprint, redirect, render_template, request, flash, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    # POST : 메모 생성
    if request.method == "POST":
        title = request.form.get('note-title')
        content = request.form.get('note-content')

        if len(title) < 1 or len(content) < 1:
            flash("제목 또는 내용이 없습니다.", category = "error")
        elif len(title) > 50:
            flash("제목이 너무 깁니다. 50자 이내", category = "error")
        elif len(content) > 2000:
            flash("내용이 너무 깁니다. 2000자 이내", category="error")
        else :            
            # Note 인스턴스 생성 -> DB에 저장
            new_note = Note(title=title, content=content, user_id=current_user.id)    
            db.session.add(new_note)
            db.session.commit()

            flash("메모 생성 완료", category="success")
            return redirect(url_for('views.home')) # 없으면 메모 계속 생성


    return render_template('home.html')


# 메모 삭제 기능
@views.route('/delete-note', methods=['POST'])
def delete_note():
    # POST : 메모 삭제
    if request.method == "POST":
        note = request.get_json()
        note_id = note.get('noteId')

        select_note = Note.query.get(note_id)
        if select_note:
            if select_note.user_id == current_user.id : 
                db.session.delete(select_note)
                db.session.commit()

        return jsonify({})
```

- `POST` 통신밖에 없겠지만, 여기선 if 해주겠습니다.
- 