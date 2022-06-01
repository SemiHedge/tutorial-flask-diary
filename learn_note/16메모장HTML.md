# 메모장 페이지 HTML
- HTML 작업이다.
- 기왕이면 즐겁게하자.. 즐겁게..

## 메모 페이지에는 무엇이 이루어져야 할까?
1. R : 지금까지 작성한 메모도 보여야되고
2. C : 새로운 메모도 생성할 수 있어야하고
3. U : (선택사항) 기존 메모 수정도 가능하고
4. D : (선택사항) 기존 메모 삭제도 가능해야한다.

- 어떤 기능이 수행될 지 생각해볼 때 기본적으로 CRUD를 고려해보고 그 다음 확장해보는 것을 추천한다.

## C : 메모 생성 영역 HTML 생성 - home.html
- `<form>` 태그와 POST통신으로 메모를 전송할 예정이다.
- bootstrap의 예를 참조
    - [ref. bootstrap 5 > form](https://getbootstrap.com/docs/5.0/forms/overview/#overview)
    - [ref. bootstrap 5 > Flating labels](https://getbootstrap.com/docs/5.0/forms/floating-labels/#example)
    - [ref. bootstrap 5 > Flating labels > textarea](https://getbootstrap.com/docs/5.0/forms/floating-labels/#textareas)


```html
{% extends "base.html" %}

{% block title %}
Title - Home
{% endblock %}

{% block content %}
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
{% endblock %}
```
- `h2`로 메모 페이지임을 표시
- `form:post`를 생성
- `input`의 name과 id를 "note-title". 이에 맞게 `label:for`도 변경
- `textarea`의 name과 id를 "note-content"로 변경. 이에 맞게 `label:for`도 변경
- 메모 저장 `button` 생성


## 메모 조회 영역 HTML 생성 - home.html 
- 부트스트랩의 `list-group`을 사용할 예정
    - [ref. bootstrap5 > list-group > custom-content](https://getbootstrap.com/docs/5.0/components/list-group/#custom-content)

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
    {% for note in user.notes %}
    <a href="#" class="list-group-item list-group-item-action">
        <div class="d-flex w-100 justify-content-between">
          <h5 class="mb-2">{{note.title}}</h5>
          <small class="text-muted">{{note.datetime}}/small>
        </div>
        <p class="mb-1">{{note.content}}</p>
    </a>  
    {% endfor %}
{% endblock %}
```

## 직접 확인해보기
- 현재는 메모 생성 영역만 보인다.
- 메모가 없기 때문에 jinja:for문이 돌지 않는다.