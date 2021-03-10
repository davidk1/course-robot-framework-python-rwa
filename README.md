# Testing ui / rest api by using robot framework and python
Implementation of real test automation framework including examples of validating web app and rest services by using robot framework and python. All tests are developed to run against helpful cypress's real world application: https://github.com/cypress-io/cypress-realworld-app. Three-tier-architecture is used to validate ui by using page objects pattern and selenium. Rest services are validated by using requests module together with different, more pythonic, approach, where most of the code is python, not robot's dsl. Also the advantage of using robot's libraries in python world is introduced. Robot's listener feature is used to demonstrate the possibility of sending individual test results to specific log management tool for the purpose of analyzing and visualising data in the dashboard.

## Installation prerequisities
- python >= 3.6
- chrome-driver version supporting your chrome-browser version: https://chromedriver.chromium.org/downloads
- chrome-driver setup: https://chromedriver.chromium.org/getting-started
- realworld-app: https://github.com/cypress-io/cypress-realworld-app
- clone the repository: 
```bash
git clone https://github.com/davidk1/course-robot-framework-python-rwa.git
```

## Installing robot framework and dependencies
```python
pip install -r requirements.txt 
```

## Run tests
ui: 
```bash
from cmd line cd to: ./ui/testsuites/rwa/tests/
run: python -m robot rwa_smoke.robot
```

api:
```bash
from cmd line cd to: ./api/testsuites/rwa/tests/
run: python -m robot rwa_api_smoke.robot
```
