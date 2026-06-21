# 실행 결과 정리. 

## pycodestyle

아래 명령어로 PEP 8 스타일을 확인했습니다.

``` bash
python -m pycodestyle budget_tracker tests setup.py
```

실행 결과:

```text
경고 없음
```

## pytest

아래 명령으로 단위 테스트를 실행합니다.

```bash
pytest
```

실행 결과:

```text
18 passed
```

## coverage

아래 명령으로 테스트 커버리지를 확인합니다.

```bash
python -m coverage run -m pytest
python -m coverage report
```

실행 결과:

```text
TOTAL 166 9 95%
```

## pip install .

아래 명령으로 패키지 설치 가능성을 확인합니다.

```bash
python -m pip install .
```

실행 결과:

```text
Successfully installed budget-tracker-seokhun-1.0.0
```
