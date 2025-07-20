# Naver Report Crawler

네이버 금융에서 기업 리포트(PDF, 투자 의견 등)를 자동으로 수집하는 파이썬 크롤러입니다.

---

## 주요 기능

- 종목명 또는 종목코드로 손쉽게 검색  
- 최신 리포트 PDF 링크/다운로드  
- 리포트 제목, 증권사, 날짜, 목표가, 투자의견 자동 추출

---

## 설치 방법

1. 레포지토리 클론 및 폴더 이동
    ```bash
    git clone https://github.com/your_id/naver_report_crawler.git
    cd naver_report_crawler
    ```

2. 필수 라이브러리 설치
    ```bash
    pip install -r requirements.txt
    ```

---

## 사용 예시

아래는 주요 기능별 파이썬 사용 예시입니다.

### 1. 종목명/코드 변환

```python
from naver_report_crawler import NaverReportCrawler

crawler = NaverReportCrawler()

# 종목명으로 코드 얻기
item_name, item_code = crawler.get_name_code("삼성전자")
print(item_name, item_code)  # 삼성전자 005930

# 종목코드로 이름 얻기
item_name, item_code = crawler.get_name_code("005930")
print(item_name, item_code)  # 삼성전자 005930

```

### 2. 상세 정보(목표가, 의견, 증권사 등) DataFrame으로 수집

```python
df_detail = crawler.get_report_detail_list(item_name="카카오", item_code="035720", start_page=1, end_page=2)
print(df_detail.head())
```

| 기업명   | 제목                    | 증권사       | 날짜        | 목표가   | 투자의견 |
|--------|-----------------------|------------|-----------|--------|--------|
| 삼성전자 | 실망감도 이미 반영된 주가   | 미래에셋증권  | 2025.07.14 | 78,000 | 매수    |
| 삼성전자 | 좋은 주식이 될 수 있다     | 대신증권      | 2025.07.09 | 74,000 | Buy    |
| 삼성전자 | 확실한 실적 바닥         | 하나증권      | 2025.07.09 | 80,000 | Buy    |
| ...    | ...                   | ...        | ...       | ...    | ...    |
| 카카오   | 가능성에 베팅             | SK증권       | 2025.07.14 | 78,000 | 매수    |
| 카카오   | B2C 영역 확장의 기점      | 교보증권      | 2025.07.09 | 68,500 | Buy    |
| ...    | ...                   | ...        | ...       | ...    | ...    |


```python
from naver_report_crawler import NaverReportCrawler
import pandas as pd

crawler = NaverReportCrawler()

# 원하는 종목명 또는 종목코드 리스트 (csv로도 확장 가능)
corp_list = ["삼성전자", "카카오"]

all_results = []
for corp in corp_list:
    item_name, item_code = crawler.get_name_code(corp)
    df = crawler.get_report_detail_list(item_name, item_code, 1, 1)
    all_results.append(df)

# 여러 종목 결과를 하나의 DataFrame으로 결합
final_df = pd.concat(all_results, ignore_index=True)
print(final_df)
```

### ㅈㅂㅈㄷ

