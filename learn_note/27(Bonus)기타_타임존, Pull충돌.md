## Pythonanywhere의 Timezone
- 만일 pythonanywhere에서 자정 시각이 안맞다면 타임존 세팅을 해주자.
- [ref. Pythonanywhere > Setting the timezone](https://help.pythonanywhere.com/pages/SettingTheTimezone/)
- `WSGI file`에 다음 코드를 추가
```python
# set timezone
import os
import time

os.environ["TZ"] = "Asia/Seoul"
time.tzset()

# basic code
import sys

# add your project directory to the sys.path
project_home = '/home/soorte/learn-flask'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from main import app as application  # noqa
```

## Pull 충돌 
`error: Your local changes to the following files would be overwritten by merge`
와 같은 에러가 나와 pull이 진행이 안된다면 다음처럼 해보자.

### 특정 파일만 pull 받기
- `git checkout {브랜치명} --파일명`

### stash를 이용하여 적용하기
1. `git stash` : 현재 Staging 영역에 있는 파일의 변경사항을 스택
2. `git pull` : 다시 git으로 최신 소스를 내려받아서, 나의 로컬PC를 최신 상태로 만듬
3. `git stash pop` : 1에서의 커밋되지않은 변경 사항을 다시 적용하고, 1을 스택에서 제거 한다.