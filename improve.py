from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv
import time

class WebScrape:
    # initialize variables
    def __init__(self, keyword):
        print("Class WebScrape initializing")
        self.p = sync_playwright().start()
        self.browser = None
        self.page = None
        self.url = None
        self.keyword= keyword
        self.job_data = {}  # 딕셔너리를 사용하여 작업 정보를 저장

    # open page
    def open_page(self, url):
        print("Operate def open_page:"+f"{self.keyword}")
        self.browser = self.p.chromium.launch(headless= False)
        self.url: str = url
        self.page = self.browser.new_page()
        self.page.goto(url)
    
    # search keyword
        #, button_tag= "button.Aside_searchButton__Xhqq3", search_bar = "검색어를 입력해 주세요."
    def search_keyword(self, button_tag= "button.Aside_searchButton__Xhqq3", search_bar = "검색어를 입력해 주세요."):
        print("Operate def serch_keyword")
        self.page.click(button_tag)
        self.page.get_by_placeholder(search_bar).fill(self.keyword)
        self.page.keyboard.down("Enter")
        self.page.click("a#search_tab_position")
        for _ in range(6):
            self.page.keyboard.down("End")
            time.sleep(1)
    
    def extract_info(self, jobs_tag = "JobCard_container__FqChn"):
        print("Operate def extract_info")
        content = self.page.content()
        self.p.stop()
        soup = BeautifulSoup(content, "html.parser")
        self.jobs = soup.find_all("div", class_ = jobs_tag)
        #print(f"jobs for {self.keyword}: {self.jobs}")
    
    def db_maker(self):
        print("Operate db_maker")
        self.job_data[self.keyword] = []  # 키워드에 대한 리스트를 딕셔너리에 저장
        
        for job in self.jobs:  
            title = job.find("strong", class_ = "JobCard_title__ddkwM").text
            link = f"https://www.wanted.co.kr{job.find('a')['href']}"
            company = job.find("span", class_ = "JobCard_companyName__vZMqJ").text
            reward = job.find("span", class_ = "JobCard_reward__sdyHn").text
            job_info = {
                "title" : title,
                "company": company,
                "reward": reward,
                "link": link
            }
            self.job_data[self.keyword].append(job_info)
            #print(f"append : {job_info}")

    def csv_maker(self):
        print(f"Operate csv_make named {self.keyword}_db.csv")
        file_name = f"{self.keyword}_jobs.csv"  # 키워드에 따라 파일 이름을 동적으로 지정
        with open(file_name, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["title", "company", "reward", "link"])
            #print("done naming")
            for job_info in self.job_data[self.keyword]:  # 키워드에 대한 작업 정보 리스트에 반복문을 수행
                #print("Inside loop")  # 반복문 내부에 들어왔는지 확인하는 디버깅 메시지
                #print(f"job_info: {job_info}")  # 작업 정보를 출력하여 확인
                writer.writerow(job_info.values())
                #print(job_info.values())
        

def main():
    keywords = ["flutter", "python", "nodejs"]

    for keyword in keywords:
        scraper = WebScrape(keyword=keyword)
        scraper.open_page("https://www.wanted.co.kr")
        scraper.search_keyword()
        scraper.extract_info()
        scraper.db_maker()
        scraper.csv_maker()

if __name__ == "__main__":
    main()

