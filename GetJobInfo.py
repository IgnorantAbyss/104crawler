from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

from GetJobList import get_job_list

def get_job_info(driver, job_list):

    links = [job["職缺URL"] for job in job_list]
    job_info = []

    for i in range(len(links)):
        try:
            driver.get(links[i])

            # 取得公司名稱
            # company_name = driver.find_element(By.CSS_SELECTOR, "div.mt-3 > a.btn-link.t3").text
            company_name_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mt-3 > a.btn-link.t3"))
            )
            company_name = company_name_element.text

            # 取得職位類別
            job_titles_elements = driver.find_elements(By.CSS_SELECTOR, "div.category-item u")
            job_titles = "、".join([element.text for element in job_titles_elements])

            # 取得薪資資訊
            # 定位包含"工作待遇"標題的h3元素，接著根據這個定位來找到相關的薪資資訊
            # //h3[contains(text(), '工作待遇')]：選擇頁面上所有包含文字"工作待遇"的<h3>元素。
            # /ancestor::div[contains(@class, 'list-row')]：向上查找這些<h3>元素最近的一個祖先<div>元素，該<div>元素的class屬性中包含"list-row"。
            # /div[contains(@class, 'list-row__data')]：在找到的<div>元素中，查找其下所有class屬性中包含"list-row__data"的子<div>元素。
            # //div[@class='t3 mb-0']/p：最後，找到這些<div>元素下所有class屬性為"t3 mb-0"的<div>元素中的<p>標籤。
            salary_blocks = driver.find_elements(By.XPATH, """//h3[contains(text(), '工作待遇')]
                                                /ancestor::div[contains(@class, 'list-row')]
                                                /div[contains(@class, 'list-row__data')]
                                                //div[@class='t3 mb-0']/p""")
            salary_info = "".join([element.text for element in salary_blocks])

            # 取得公司地址
            # 定位包含具體地址信息的<span>標籤
            address_span = driver.find_element(By.CSS_SELECTOR, "div.job-address > span")
            address_text = address_span.text
            # 初始化附加信息文本
            additional_info_text = ""
            # 使用find_elements檢查是否存在包含附加地址信息的<span>標籤（例如距離捷運站信息）
            additional_info_spans = driver.find_elements(By.CSS_SELECTOR, "div.job-address > span.t4")
            if additional_info_spans:
                # 如果列表不為空，則表示找到了元素
                additional_info_text = additional_info_spans[0].text
            # 合併地址信息和附加信息
            work_address = f"{address_text} {additional_info_text}".strip()

            # 取得工作內容
            job_content = driver.find_element(By.CSS_SELECTOR, 'div.job-description > p.job-description__content').text

            # 取得語文條件
            # 定位文本內容包含"語文條件"的<h3>元素，..向上找到父元素後選擇<div>類型的同級元素，//p選擇所有<p>子元素
            language_requirements_elements = driver.find_elements(By.XPATH, "//h3[contains(text(), '語文條件')]/../following-sibling::div//p")

            if len(language_requirements_elements) > 0:
                language_requirements = "、".join([element.text for element in language_requirements_elements])

            # 取得擅長工具條件
            # 定位文本內容包含"擅長工具"的<h3>元素，..向上找到父元素後選擇<div>類型的同級元素，//u選擇所有<u>子元素
            tools_requirements_elements = driver.find_elements(By.XPATH, "//h3[contains(text(), '擅長工具')]/../following-sibling::div//u")

            if len(tools_requirements_elements) > 0:
                tools_requirements = "、".join([element.text for element in tools_requirements_elements])
            else:
                tools_requirements = driver.find_element(By.XPATH, "//h3[contains(text(), '擅長工具')]/../following-sibling::div").text

            # 取得工作技能條件
            # 定位文本內容包含"工作技能"的<h3>元素，..向上找到父元素後選擇<div>類型的同級元素，//u選擇所有<u>子元素
            skill_requirements_elements = driver.find_elements(By.XPATH, "//h3[contains(text(), '工作技能')]/../following-sibling::div//u")

            if len(skill_requirements_elements) > 0:
                skill_requirements = "、".join([element.text for element in skill_requirements_elements])
            else: 
                # 找到包含"工作技能"的<h3>元素後，ancestor向上找到父輩元素中class屬性包含list-row的<div>元素，然後向下尋找包含list-row__data的<div>元素，最後定位到div內的文本
                skill_requirements = driver.find_element(By.XPATH, """//h3[contains(text(), '工作技能')]
                                                        /ancestor::div[contains(@class, 'list-row')]//
                                                        div[contains(@class, 'list-row__data')]/div""").text
                
            # 取得其他條件
            # 定位文本內容包含"其他條件"的<h3>元素，..向上找到父元素後選擇<div>類型的同級元素，//u選擇所有<p>子元素
            other_requirements_elements = driver.find_elements(By.XPATH, "//h3[contains(text(), '其他條件')]/../following-sibling::div//p")
            if len(other_requirements_elements) > 0:
                other_requirements = "\n".join([element.text for element in other_requirements_elements])
            else:
                other_requirements = "沒有找到相關的其他條件。"

            job_info_dict = {
                "公司名稱" : company_name,
                "職務類別" : job_titles,
                "工作待遇" : salary_info,
                "上班地點" : work_address,
                "工作內容" : job_content,
                "語文條件" : language_requirements,
                "擅長工具要求" : tools_requirements,
                "工作技能" : skill_requirements,
                "其他條件" : other_requirements
                }
            
            job_info.append(job_info_dict)

        
        except Exception as e:
            print(f"發生錯誤，網址：{links[i]} 錯誤信息：{e}")
            
            # 錯誤處理：重新打開瀏覽器窗口顯示出錯網頁
            driver.quit()  # 首先關閉無頭模式的瀏覽器實例
            debug_driver = webdriver.Chrome()  # 使用非無頭模式
            debug_driver.get(links[i])  # 導航到出錯的網址
            

    driver.quit()
    job_info_df = pd.DataFrame(job_info)
    return job_info_df

if __name__ == "__main__":
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)# 使用無頭模式
    driver.set_window_size(1920, 1080) # 設置窗口大小為1920x1080

    url = 'https://www.104.com.tw/jobs/search/?jobsource=index_s&keyword=AI&mode=s&page=1'

    job_list = get_job_list(driver, url, pages=0)
    for job in job_list:
        print(job)

    driver = webdriver.Chrome(options=options)# 使用無頭模式
    driver.set_window_size(1920, 1080) # 設置窗口大小為1920x1080
    job_info_df = get_job_info(job_list=job_list, driver=driver)

    print(job_info_df)

