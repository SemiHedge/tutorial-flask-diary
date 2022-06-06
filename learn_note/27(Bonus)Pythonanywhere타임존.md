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