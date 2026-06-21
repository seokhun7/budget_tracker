# budget_tracker

## 1. 프로젝트 개요

`budget_tracker`는 일별 수입과 지출을 기록하고, 카테고리별 통계와
월간 리포트를 생성하는 Python 패키지입니다. `Transaction` 부모
클래스가 공통 검증과 직렬화를 담당하고, `Income`과 `Expense`가
각각 수입과 지출의 세부 동작을 담당합니다.

## 2. 설치 방법

새 가상환경에서 다음 명령으로 설치할 수 있습니다.

```bash
python -m pip install --upgrade pip
python -m pip install .
```

개발 도구까지 함께 설치하려면 다음 명령을 사용합니다.

```bash
python -m pip install ".[dev]"
```

## 3. 빠른 시작

```python
from budget_tracker import BudgetTracker

tracker = BudgetTracker()
tracker.add_income(3000000, "salary", "2026-05-01", "monthly salary")
tracker.add_expense(12000, "food", "2026-05-02", "lunch")

report = tracker.monthly_report(2026, 5)
print(report["income"])
print(report["expense"])
print(report["balance"])
```

## 4. 주요 기능

- 일별 수입과 지출 기록
- `Income`, `Expense` 하위 클래스를 활용한 객체지향 설계
- 금액, 날짜, 카테고리, 설명 입력값 검증
- 카테고리별 수입과 지출 합계 계산
- 월간 총수입, 총지출, 잔액, 거래 목록 리포트 생성
- 테스트 커버리지와 GitHub Actions CI 예시 제공

## 5. 테스트 실행 방법

```bash
python -m pip install ".[dev]"
python -m pycodestyle budget_tracker tests setup.py
pytest
python -m coverage run -m pytest
python -m coverage report
```

현재 확인한 실행 결과 요약은 `results.md`에 정리되어 있습니다.

## 6. 작성자 정보

- 작성자: 홍석훈
- 패키지명: `budget_tracker`
- GitHub URL: https://github.com/seokhun7/budget_tracker.git

## 지원 카테고리

수입 카테고리는 `salary`, `bonus`, `gift`, `allowance`를 지원합니다.
지출 카테고리는 `food`, `housing`, `transport`, `utility`, `health`,
`education`을 지원합니다.
