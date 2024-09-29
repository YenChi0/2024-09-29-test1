from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
#讓程式可以按鍵盤上按鍵 使用方法(以enter為例): search.send_keys(keys.RETURN)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
options = Options()
options.chrome_driver_path = 'C:/Users/clair/chromedriver.exe'
driver = webdriver.Chrome(options=options)
driver.get('https://demo.opencti.io/dashboard')
time.sleep(3)
login_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[3]/a")
login_button.click()
time.sleep(3)
#輸入帳號密碼
ac = driver.find_element(By.NAME, "username")
ac.click()
ac.send_keys("411580049@m365.fju.edu.tw")
time.sleep(3)
pw = driver.find_element(By.NAME, "password")
pw.click()
pw.send_keys("77654857")
time.sleep(3)
conti = driver.find_element(By.NAME, "action")
conti.click()
time.sleep(8)
#搜尋
def search():
    search = driver.find_element(By.NAME, "keyword")
    search.click()
    search.send_keys("STIX URL")
    search.send_keys(Keys.RETURN)  # 按下 Enter 鍵
    time.sleep(7)
    search.click()
    search.clear()

search()
#算出一頁有幾筆資料
count = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[2]/div[1]/div/div[2]/div[1]/div/div/p/span[1]")
counttext = count.text
# 使用 split() 方法分隔字符串
parts = counttext.split("-")
# 提取最後一個部分並轉換為整數
countnum = int(parts[-1])
print(countnum)
#找不到元素時滾動視窗
def scroll_until_element_found(driver, by, value, max_attempts=10, scroll_pause_time=1):
    element = None
    attempts = 0
    while attempts < max_attempts:
        try:
            # 嘗試找到元素
            element = driver.find_element(by, value)
            #print("元素已找到！")
            break  # 找到元素，退出循環
        except:
            # 如果沒找到，向下滾動頁面
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            attempts += 1
            time.sleep(scroll_pause_time)  # 等待頁面加載
            print(f"嘗試次數: {attempts}，未找到元素，繼續滾動...")

    if element is None:
        print("已達到最大嘗試次數，未能找到元素。")
    return element
#找資料
n=1
while(True):
    if n>countnum:
        break
    nextbutton = scroll_until_element_found(driver, By.XPATH, f"/html/body/div[1]/div/main/div[3]/div[2]/div[{n}]/div[10]/button", max_attempts=20)
    nextbutton.click()
    time.sleep(8)
    data = {}
    # 設置等待時間（最多等待10秒）
    wait = WebDriverWait(driver, 10)
    try:
        # 等待該元素可見，直到指定的 XPATH 匹配到元素
        urldata = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[4]/div[1]/div/div/div[1]/div[2]/pre/div")
        #data["URL"] = urldata.text
        urldescription = driver.find_element(By.XPATH,"/html/body/div[1]/div/main/div/div[4]/div[1]/div/div/div[1]/div[1]/div/div/div/div/p")
        #data["Description"] = urldescription.text
        #print("找到元素！")
    except:
        urldescription = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div[4]/div[1]/div/div/div[1]/div[1]/div/div")
        #data["Description"] = "No Description."
    finally:
        print(f"{n} URL : {urldata.text}, {urldescription.text}")
        #print(data)
        time.sleep(8)
        n += 1
        search()
