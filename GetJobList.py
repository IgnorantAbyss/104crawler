from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

# def get_job_info(driver, url):
#     driver.get(url) # 打開職缺資訊頁面
#     wait = WebDriverWait(driver, 5)

#     company_name = driver.find_element(By.CSS_SELECTOR, "选择器").text
#     job_category = driver.find_element(By.CSS_SELECTOR, "选择器").text
#     salary = driver.find_element(By.CSS_SELECTOR, "选择器").text
#     work_location = driver.find_element(By.CSS_SELECTOR, "选择器").text
#     job_content = driver.find_element(By.CSS_SELECTOR, "选择器").text
#     qualification = driver.find_element(By.CSS_SELECTOR, "选择器").text

#     job_info = {
#         "公司名稱",
#         "職務類別",
#         "工作待遇",
#         "上班地點",
#         "工作內容",
#         "條件要求"
#         }

def get_job_list(driver, url, pages):

    driver.get(url)  # 打開職缺列表頁面

    # 等待初次頁面加載完畢
    wait = WebDriverWait(driver, 5)  # 使用WebDriverWait而非固定時間等待，最長等待時間5秒

    for _ in range(pages):
            # 執行JavaScript腳本，滾動到頁面底部
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # 等待新加載的內容出現

    # 定位所有的職缺<article>元素
    job_elements = driver.find_elements(By.CSS_SELECTOR, 'article.js-job-item')
    JobList = []  # 改為使用列表來存儲多條職缺資訊
    # 遍歷找到的職缺元素
    for job_element in job_elements:
        # 檢查職缺元素內的<b-tit__date>是否包含特定的SVG圖標
        ad_icons = job_element.find_elements(By.CSS_SELECTOR, 'span.b-tit__date svg')
        
        # 如果沒有找到SVG圖標，表示非廣告職缺
        if len(ad_icons) == 0:
            job_title = job_element.find_element(By.CSS_SELECTOR, 'a.js-job-link').text
            job_link = job_element.find_element(By.CSS_SELECTOR, 'a.js-job-link').get_attribute('href')
            JobList.append({"職缺名稱": job_title, "職缺URL": job_link})  # 添加一條職缺資訊到列表中
            # JobList.append(job_link)
    
    driver.quit()

    return JobList

if __name__ == "__main__":
    driver = webdriver.Chrome()  # 根據您的瀏覽器選擇WebDriver
    url = 'https://www.104.com.tw/jobs/search/?jobsource=index_s&keyword=AI&mode=s&page=1'
    job_list = get_job_list(driver, url, pages=3)
    for job in job_list:
        print(job)