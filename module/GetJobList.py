from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

def get_job_list(keyword, location, custom_pages=False, driver=False):
    # 預設Driver
    if not driver:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        driver = webdriver.Chrome(options=options)# 使用無頭模式
        driver.set_window_size(1920, 1080) # 設置窗口大小為1920x1080
    # 區域代碼
    location_dict = {
        "台北市":6001001000,
        "新北市":6001002000,
        "宜蘭縣":6001003000,
        "基隆市":6001004000,
        "桃園市":6001005000,
        "新竹縣市":6001006000,
        "苗栗縣":6001007000,
        "台中市":6001008000,
        "彰化縣":6001010000,
        "南投縣":6001011000,
        "雲林縣":6001012000,
        "嘉義縣市":6001013000,
        "台南市":6001014000,
        "高雄市":6001016000,
        "屏東縣":6001018000,
        "台東縣":6001019000,
        "花蓮縣":6001020000,
        "澎湖縣":6001021000,
        "金門縣":6001022000,
        "連江縣":6001023000
        }
    
    # 打開104網頁
    driver.get("https://www.104.com.tw/jobs/main/")

    # 等待頁面加載完成
    wait = WebDriverWait(driver, 5)

    # 搜尋框
    # 定位到搜尋輸入框
    search_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.form-control")))
    # 清除搜尋框中的內容並輸入搜尋關鍵字
    search_input.clear()
    search_input.send_keys(keyword)
    print(f"輸入關鍵字 '{keyword}' 完成")
    # 區域選擇
    # 等待並點擊顯示區域選擇表單的按鈕
    show_form_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., '地區')]")))
    show_form_button.click()
    # 選擇第一層的區域 (例如：台灣地區)
    taiwan_region = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.category-item--level-one:nth-child(1)")))
    taiwan_region.click()
    # 選擇第二層的地區 
    # 使用JavaScript點擊checkbox
    driver.execute_script(f"document.querySelector('input[type=\"checkbox\"][value=\"{location_dict[location]}\"]').click()")
    # 最後點擊確定按鈕
    confirm_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.category-picker-btn-primary")))
    confirm_button.click()

    print(f"選擇地區{location}完成")
    # 執行搜尋
    # 定位到搜尋按鈕並點擊
    search_button = driver.find_element(By.CSS_SELECTOR, "div.col.col-2 > button.btn.btn")
    search_button.click()
    print(f"執行搜尋")

    # 等待初次頁面加載完畢
    wait = WebDriverWait(driver, 5)  # 使用WebDriverWait而非固定時間等待，最長等待時間5秒
    print(f"搜尋 '{location} {keyword}' 頁面讀取完成")

    def click_load_more():
        try:
            load_more_button = driver.find_element(By.CSS_SELECTOR, '.js-more-page')
            driver.execute_script("arguments[0].click();", load_more_button)
            time.sleep(1)  # 等待載入完成
        except NoSuchElementException:
            print("無法手動加載")
            time.sleep(1)
            pass

    # 頁面總數
    if custom_pages:
        for _ in range(custom_pages):
           if _ >= 15:
               click_load_more()
           # 執行JavaScript腳本，滾動到頁面底部
           driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
           time.sleep(1.5)
        print(f"本次搜尋共{custom_pages}頁")
    
    else:
        # 找到 page-select 元素
        page_element = driver.find_element(By.CSS_SELECTOR, '.page-select')
        # 找到 select 元素中的所有 option
        options = page_element.find_elements(By.TAG_NAME, 'option')
        # 提取最高頁數
        if options:
            highest_page = max(int(option.get_attribute('value')) for option in options)
        else:
            highest_page = 1  # 設置預設值
        print(f"本次搜尋共{highest_page}頁")
        for _ in range(highest_page):
                if _ >= 15:
                    click_load_more()
                # 執行JavaScript腳本，滾動到頁面底部
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1.5)
        

    # 定位所有的職缺<article>元素
    job_elements = driver.find_elements(By.CSS_SELECTOR, '#js-job-content > *')
    job_list = []  # 使用列表來存儲多條職缺資訊
    # 遍歷找到的職缺元素
    for job_element in job_elements:
        # 檢查是否為無數據的節點
        if 'job-list-item b-block--nodata b-pos-relative js-job-personal' in job_element.get_attribute('class'):
            print("搜尋結果過少，後續為推荐工作")
            break

        # 檢查是否為職缺項目
        if 'job-list-item' in job_element.get_attribute('class'):
            # 檢查職缺元素內的 <span> 是否包含特定的 SVG 圖標
            ad_icons = job_element.find_elements(By.CSS_SELECTOR, 'span.b-tit__date svg')
            # 如果沒有找到 SVG 圖標，表示非廣告職缺
            if len(ad_icons) == 0:
                try:
                    job_topic = job_element.find_element(By.CSS_SELECTOR, 'a.js-job-link').text
                    job_link = job_element.find_element(By.CSS_SELECTOR, 'a.js-job-link').get_attribute('href')
                except Exception:
                    job_topic = None
                    job_link = None
                if job_topic and job_link:
                    job_list.append({"職缺標題": job_topic, "職缺URL": job_link})
                # JobList.append(job_link)
    print(f"搜尋完成，本次搜尋共有{len(job_list)}筆職缺資料")
    driver.quit()

    return job_list

# if __name__ == "__main__":
#     driver = webdriver.Chrome()  # 根據您的瀏覽器選擇WebDriver
#     keyword = '數據工程師'
#     # job_list = get_job_list(driver, keyword, location="台北市", custom_pages=3)
#     job_list = get_job_list(keyword, location="連江縣", driver=driver)
#     for job in job_list:
#         print(job)