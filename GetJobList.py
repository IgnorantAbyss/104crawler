from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import time


def get_job_list(driver, keyword, pages):

    # 打開104網頁
    driver.get("https://www.104.com.tw/jobs/main/")

    # 等待頁面加載完成
    wait = WebDriverWait(driver, 5)

    # 定位到搜尋輸入框
    search_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.form-control")))

    # 清除搜尋框中的內容（如果有）並輸入搜尋關鍵字
    search_input.clear()
    search_input.send_keys(keyword)

    # 定位到搜尋按鈕並點擊
    search_button = driver.find_element(By.CSS_SELECTOR, "div.col.col-2 > button.btn.btn")
    search_button.click()

    # 等待初次頁面加載完畢
    wait = WebDriverWait(driver, 5)  # 使用WebDriverWait而非固定時間等待，最長等待時間5秒

    for _ in range(pages):
            # 執行JavaScript腳本，滾動到頁面底部
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # 等待新加載的內容出現

    # 定位所有的職缺<article>元素
    job_elements = driver.find_elements(By.CSS_SELECTOR, 'article.js-job-item')
    job_list = []  # 改為使用列表來存儲多條職缺資訊
    # 遍歷找到的職缺元素
    for job_element in job_elements:
        # 檢查職缺元素內的<b-tit__date>是否包含特定的SVG圖標
        ad_icons = job_element.find_elements(By.CSS_SELECTOR, 'span.b-tit__date svg')
        
        # 如果沒有找到SVG圖標，表示非廣告職缺
        if len(ad_icons) == 0:
            job_topic = job_element.find_element(By.CSS_SELECTOR, 'a.js-job-link').text
            job_link = job_element.find_element(By.CSS_SELECTOR, 'a.js-job-link').get_attribute('href')
            job_list.append({"職缺標題": job_topic, "職缺URL": job_link})  # 添加一條職缺資訊到列表中
            # JobList.append(job_link)
    
    driver.quit()

    return job_list

if __name__ == "__main__":
    driver = webdriver.Chrome()  # 根據您的瀏覽器選擇WebDriver
    keyword = 'AI'
    job_list = get_job_list(driver, keyword, pages=3)
    for job in job_list:
        print(job)