## pythonanywhere로 배포하기
- heroku로 배포하려하니, 무료의 경우 DB가 적다.
    - 5MB 지원. 대략 텍스트 400만자 작성하면 끝난다고.. 꽤 되나?
- 그래도 pythonanywhere의 DB용량과 비교하면 좀 크다.

## 회원가입은 알아서
- https://www.pythonanywhere.com/

## 로그인 이후 배포 하기(파일 업로드로 하기)
1. 클릭 : 상단 WEB 메뉴
2. 클릭 : `Add a new web app` 
3. 클릭 : Next > Flask > 개발할 때 Python 버전과 유사한 것
4. Path 입력 : `/home/{여러분id}/mysite/main.py` 로 변경 후 Next클릭
5. 클릭 : 상단 File 메뉴 > mysite 폴더
6. 압축 : 개발한 Flask APP과 관련된 폴더 파일 압축하여 `flask_app.zip` 생성 후 업로드
7. 클릭 : 상단 Console 메뉴 > Other:Bash
8. 이동 : `cd mysite`
9. 압축풀기 : `unzip flask_app.zip .` > 중복 물어보면 `y` 입력
10. (선택) 가상환경을 원한다면 가이드 참조
    - https://help.pythonanywhere.com/pages/Virtualenvs
    - https://help.pythonanywhere.com/pages/Flask/
    - `mkvirtualenv --python=/usr/bin/python3.9 my-virtualenv`
    - 아까 선택한 python 버전을 선택
    - `pip3 install flask flask-login flask-sqlalchemy`
    - `pip3 list`로 설치 확인
11. 클릭 : 상단 메뉴 Web > `Reload ...` > `{유저명}.pythonanywhere.com`
    - 접속이 잘 되었다면, 로그인 등의 기능을 확인하자
12. (만일 안된다면) `WSGI configuration file` 설정
    - FLASK APP의 변수를 지정해야하는데, 지금까지 잘 했으면 다음과 같을 것
```python
import sys

# add your project directory to the sys.path
project_home = '/home/{여러분id}/mysite'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from main import app as application  # noqa
```

## Github을 통해서 하기
- 위의 방법에서 파일을 업로드 하는 과정만 바뀝니다.
1. 클릭 : 상단 WEB 메뉴
2. 클릭 : `Add a new web app` 
3. 클릭 : Next > Flask > 개발할 때 Python 버전과 유사한 것
4. Path 입력 : `/home/{여러분id}/{여러분Repository이름}/main.py` 로 변경 후 Next클릭
5. 클릭 : 상단 Console 메뉴 > Other:Bash
6. 클론 : `git clone 레포지토리_주소`
7. (선택) 가상환경을 원한다면 가이드 참조
    - https://help.pythonanywhere.com/pages/Virtualenvs
    - https://help.pythonanywhere.com/pages/Flask/
    - `mkvirtualenv --python=/usr/bin/python3.9 my-virtualenv`
    - 아까 선택한 python 버전을 선택
    - `pip3 install flask flask-login flask-sqlalchemy`
    - `pip3 list`로 설치 확인
8. 클릭 : 상단 메뉴 Web > `Reload ...` > `{유저명}.pythonanywhere.com`
    - 접속이 잘 되었다면, 로그인 등의 기능을 확인하자
9. (만일 안된다면) `WSGI configuration file` 설정
    - FLASK APP의 변수를 지정해야하는데, 지금까지 잘 했으면 다음과 같을 것

```python
import sys

# add your project directory to the sys.path
project_home = '/home/{여러분계정}/{여러분repository이름}'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from main import app as application  # noqa
```

###  만일 4번 6번의 순서를 바꿔서 실행했다면?
- Repository에서 최신 커밋 정보를 가져와서 HEAD를 옮긴 후 Pull

1. `git fetch --all`
    - `git pull`을 하기 위해서 깃허브의 repository에서 커밋 정보를 확인
2. `git reset --hard origin/main`
    - `git reset`을 통해 `head`를 최신 commit을 가리킴
3. `git pull`
    - 최신 커밋으로 덮어쓰기