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

아래 코드를 실행하면 원하는 종목의 최신 리포트 정보를 한 번에 수집할 수 있습니다.

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
