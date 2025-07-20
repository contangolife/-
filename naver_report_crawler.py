# naver_report_crawler.py
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pykrx import stock
import pandas as pd
from tqdm import tqdm
import re
import time

class NaverReportCrawler:
    def __init__(self):
        df = stock.get_market_ticker_list(market="ALL")
        df_info = pd.DataFrame({
            "종목코드": df,
            "회사명": [stock.get_market_ticker_name(code) for code in df]
        })
        self.name2code = dict(zip(df_info['회사명'], df_info['종목코드']))
        self.code2name = dict(zip(df_info['종목코드'], df_info['회사명']))
        self.base_url = "https://finance.naver.com"

    def get_name_code(self, input_val):
        input_val = input_val.strip()
        if input_val.isdigit() and len(input_val) == 6:
            item_name = self.code2name.get(input_val)
            if item_name:
                return item_name, input_val
            else:
                print(f"[오류] 종목코드 '{input_val}'에 해당하는 종목명이 없습니다.")
                return "", ""
        else:
            item_code = self.name2code.get(input_val)
            if item_code:
                return input_val, item_code
            else:
                print(f"[오류] 종목명 '{input_val}'에 해당하는 종목코드가 없습니다.")
                return "", ""

    def get_pdf_links(self, item_input, page_from=1, page_to=4, verbose=True):
        item_name, item_code = self.get_name_code(item_input)
        if not item_name or not item_code:
            print("입력값을 다시 확인해주세요.")
            return pd.DataFrame(columns=["PDF 링크"])

        pdf_links = []
        for page in range(page_from, page_to+1):
            url = f"{self.base_url}/research/company_list.naver?searchType=itemCode&itemName={item_name}&itemCode={item_code}&page={page}"
            res = requests.get(url)
            soup = BeautifulSoup(res.content, "html.parser")
            for a_tag in soup.find_all("a", href=True):
                href = a_tag['href']
                if href.endswith(".pdf"):
                    full_link = urljoin(self.base_url, href)
                    pdf_links.append(full_link)
            if verbose:
                print(f"Page {page}에서 {len(pdf_links)}건 누적 추출됨")
        df = pd.DataFrame(pdf_links, columns=["PDF 링크"])
        return df
        
    def download_pdfs(self, df, item_name=None, folder_path=None):
        # 1. 폴더명 결정
        if folder_path is None:
            if item_name:
                folder_path = f"{item_name}_리포트_pdf/"
            else:
                folder_path = "리포트_pdf/"
        os.makedirs(folder_path, exist_ok=True)
        saved_count = 0
    
        # 2. tqdm 적용: 전체 개수 기준
        for i, url in enumerate(tqdm(df.iloc[:, 0], desc="PDF 다운로드", unit="개", ncols=80), 1):
            file_name = f"report_{i}.pdf"
            save_path = os.path.join(folder_path, file_name)
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    saved_count += 1
            except Exception as e:
                tqdm.write(f"[오류] {file_name}: {e}")
    
        print(f"\n총 {saved_count}개 저장 완료 (폴더: {folder_path})")

    def get_report_detail_list(self, item_name, item_code, start_page=1, end_page=3):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        results = []
        for i in range(start_page, end_page + 1):
            url = f"https://finance.naver.com/research/company_list.naver?keyword=&brokerCode=&writeFromDate=&writeToDate=&searchType=itemCode&itemName={item_name}&itemCode={item_code}&page={i}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 상세링크만 미리 리스트로 추출
            report_links = [
                (a_tag.get_text(strip=True), 'https://finance.naver.com/research/' + a_tag['href'])
                for a_tag in soup.find_all("a", href=True)
                if re.match(r"^company_read\.naver\?", a_tag['href'])
            ]
            
            # tqdm으로 상세페이지 반복
            for title, detail_url in tqdm(report_links, desc=f"{i}페이지", leave=False):
                detail_resp = requests.get(detail_url, headers=headers)
                detail_soup = BeautifulSoup(detail_resp.text, 'html.parser')
    
                securities_firm, date = None, None
                source = detail_soup.find('p', class_='source')
                if source:
                    text = source.get_text('|', strip=True)
                    items = [item.strip() for item in text.split('|') if item.strip()]
                    if len(items) >= 2:
                        securities_firm = items[0]
                        date = items[1]
    
                target_price, strong = None, None
                div1 = detail_soup.find('div', class_='view_info_1')
                if div1:
                    strong = div1.find('strong')
                    if strong:
                        target_price = strong.get_text(strip=True)
    
                opinion = None
                if strong and strong.parent:
                    for sib in strong.parent.next_siblings:
                        if getattr(sib, 'name', None) == 'em' and 'coment' in sib.get('class', []):
                            opinion = sib.get_text(strip=True)
                            break
    
                results.append({
                    '기업명':item_name,
                    '제목': title,
                    '링크': detail_url,
                    '증권사': securities_firm,
                    '날짜': date,
                    '목표가': target_price,
                    '투자의견': opinion
                })
                time.sleep(0.3)  
    
        return pd.DataFrame(results)

    


