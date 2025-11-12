import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#智慧等待相關套件
#-------------------------------------------------------------
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
#-------------------------------------------------------------
from selenium.webdriver.common.by import By 
#-------------------------------------------------------------
def scrape_latest_books():
    # 建立 chrome_options 物件，用於配置 chrome 選項
    Chrome_options = Options()
    Chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=Chrome_options)
    browser.get("https://www.books.com.tw/")
    print(browser.title)  # 印出網頁標題確認成功載入
    wait = WebDriverWait(browser, 10)
#-------------------------------------------------------------
    all_books_data = []
    try:
        # 找到搜尋框並輸入關鍵字
        element = browser.find_element(By.ID, "key")
        print("找到搜尋框元素:")
        element.send_keys("LLM")
        print("已輸入關鍵字 LLM")
        element.submit()
        print("已提交搜尋表單")
#-------------------------------------------------------------
        # 點擊圖書標籤
        label = browser.find_element(By.XPATH, "//label[@class='container2' and contains(text(),'圖書')]")# 找到圖書標籤元素尋找標籤label並且class為container2且內文包含圖書
        time.sleep(8)
        browser.execute_script("arguments[0].click();", label)# 使用 JavaScript 點擊標籤 arguments[0] 是在 execute_script() 方法裡傳給 JavaScript 腳本的第一個物件或值
        time.sleep(5)
        print("(頁面已重新載入)")
        
#-------------------------------------------------------------
        # 偵測總頁數
        total_pages = 1  # 預設為 1 頁
        try:
            selected_option = browser.find_element(By.CSS_SELECTOR, "#page_select > option[selected]")#定位到目前被選中的頁數選項
            selected_text = selected_option.text
            match = re.search(r'\d+', selected_text)# 使用正則表達式從選項文字中提取數字
            #取得總頁數
            if match:
                total_pages = int(match.group(0))
        except Exception as e:
            print("(找不到總頁數資訊")
        print(f"偵測到總共有 {total_pages} 頁。")
#-------------------------------------------------------------
        # 開始逐頁爬取
        for current_page in range(1, total_pages + 1):
            print(f"正在爬取第 {current_page} / {total_pages} 頁...") 
            try:
                #定位書籍容器
                book_container_css = "div[id^='prod-itemlist-']"
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, book_container_css)))#智慧等待書籍容器出現 我在寫的時候遇到過因為網頁載入較慢導致找不到元素的情況 詢問ai後加上這行解決了原本使用time.sleep()有秒數不穩定的問題
                book_containers = browser.find_elements(By.CSS_SELECTOR, book_container_css)
#-------------------------------------------------------------
                # 提取每本書的資訊
                for container in book_containers:

                    try:
                        title_element = container.find_element(By.CSS_SELECTOR, "h4 > a")
                        full_title = title_element.get_attribute("title")
                    except Exception as e:
                        full_title = "N/A" # 找不到書名

                    try:
                        author_element = container.find_element(By.CLASS_NAME, "author")#定位作者元素
                        author_links = author_element.find_elements(By.TAG_NAME, "a")#取得作者元素中所有作者連結
                        
                        if author_links:
                            author_names_list = [link.text for link in author_links if link.text]#提取每個作者連結的文字並組成清單

                            author_name = ", ".join(author_names_list)#將多個作者名稱以逗號分隔
                    except Exception as e:
                        author_name = "N/A" # 找不到作者
                    try:
                        price_element = container.find_element(By.CLASS_NAME, "price")
                        price=price_element.text
                       
                        price_match = re.search(r'(\d+)\s*元', price.replace(' ', ''))#處理價格字串
                         #處理成整數
                        if price_match:
                            price = int(price_match.group(1))
                    except Exception as e:
                        price = "N/A" # 找不到價格
                    try:
                        link_element = container.find_element(By.CSS_SELECTOR, "h4 > a")
                        link=link_element.get_attribute("href")
                    except Exception as e:
                        link = "N/A" # 找不到連結
                    if full_title != "N/A":
                        all_books_data.append({'title': full_title, 'author': author_name , 'price': price , 'link': link})
            except Exception as e:
                print(f"  > 抓取書籍資訊時發生錯誤: {e}")
#------------------------------------------------------------- 也是有time.sleep()有秒數不穩定的問題為了確保每頁都能正確載入改用智慧等待否則會有抓不到書籍的情況 
            # ★★★★★★★★★ 換頁 ★★★★★★★★★
            if current_page < total_pages:
                try:
                    stale_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, book_container_css)))#等待目前頁面的書籍容器元素變為陳舊狀態
                    next_page_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "next")))#等待下一頁按鈕可點擊
                     #使用 JavaScript 點擊下一頁按鈕
                    browser.execute_script("arguments[0].click();", next_page_button)
                    wait.until(EC.staleness_of(stale_element))#等待目前頁面的書籍容器元素變為陳舊狀態，表示頁面已經開始重新載入
                except Exception as e:
                    print("無法找到下一頁按鈕或點擊失敗:", e)
                    break
#-------------------------------------------------------------
    except Exception as e:
        print("找不到搜尋框元素:", e)
#-------------------------------------------------------------
# 關閉瀏覽器
    finally:
        print("爬取完成。")
        browser.quit()
        return all_books_data
#---------------------------------------------
# 單獨測試 scraper.py 時執行以下程式碼
'''if __name__ == "__main__":
    print("--- 正在單獨測試 scraper.py ---")
    books = scrape_latest_books()  # 獲取書籍資料
    print(f"總共抓到 {len(books)} 本書：")
    for i, book in enumerate(books[:5]): 
        print(f"{i+1}. {book['title']} by {book['author']} - {book['price']} 連結: {book['link']}")'''