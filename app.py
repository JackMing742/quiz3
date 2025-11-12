import scraper
import database
import time
#-----------------------------------------------------
def main():
    while True:
        #根據使用者選單選項執行不同功能
        print("----- 博客來 LLM 書籍管理系統 -----")
        print("1. 更新書籍資料庫")
        print("2. 查詢書籍")
        print("3. 離開")
        print("----------------------------------" )
        choice = input("請輸入選項 (1-3): ")
#-----------------------------------------------------
# 更新書籍資料庫
        if choice == '1':
            print("開始從網路爬取最新書籍資料...")
            books_data = scraper.scrape_latest_books()
            print(f"共抓取到 {len(books_data)} 本書籍資料。")
            database.sql_create()
            new_count = database.save_books(books_data)
            print(f"成功新增 {new_count} 本新書籍到資料庫中。")
#-----------------------------------------------------
# 查詢書籍
        elif choice == '2':
            #根據使用者選單選項執行不同查詢功能
            while True:
                print("----- 查詢書籍 -----")
                print("a. 依書名查詢")
                print("b. 依作者查詢")
                print("c. 返回主選單")
                print("----------------------------------" )
                choice = input("請輸入選項 (a-c): ")
                #-----------------------------------------------------
                if choice == 'a':
                    title_keyword = input("請輸入書名關鍵字: ")
                    #連線到資料庫並執行查詢
                    conn = database.sqlite3.connect(database.db_name)
                    cursor = conn.cursor()
                    cursor.execute("SELECT title, author, price, link FROM llm_books WHERE title LIKE ?", ('%' + title_keyword + '%',))
                    results = cursor.fetchall()
                    conn.close()#關閉資料庫連線
                    #-------------------------------------------------
                    #顯示查詢結果
                    if results:
                        print(f"找到 {len(results)} 本書籍：")
                        for row in results:
                            print(f"書名: {row[0]}, 作者: {row[1]}, \n價格: {row[2]}, \n連結: {row[3]}")
                    else:
                        print("沒有找到相關書籍。")
            #-----------------------------------------------------
                elif choice == 'b':
                    author_keyword = input("請輸入作者關鍵字: ")
                    #連線到資料庫並執行查詢
                    conn = database.sqlite3.connect(database.db_name)
                    cursor = conn.cursor()
                    cursor.execute("SELECT title, author, price, link FROM llm_books WHERE author LIKE ?", ('%' + author_keyword + '%',))
                    results = cursor.fetchall()
                    conn.close()#關閉資料庫連線
                    #-------------------------------------------------
                    #顯示查詢結果
                    if results:
                        print(f"找到 {len(results)} 本書籍：")
                        for row in results:
                            print(f"書名: {row[0]}, 作者: {row[1]},\n 價格: {row[2]},\n 連結: {row[3]}")
                    else:
                        print("沒有找到相關書籍。")
            #-----------------------------------------------------
                elif choice == 'c':
                    break
                else:
                    print("無效的選項，請重新輸入。")
#-----------------------------------------------------
# 離開程式
        elif choice == '3':
            print("感謝使用，再見！")
            break
        else:
            print("無效的選項，請重新啟動程式並選擇 1-3 之間的選項。")
#-----------------------------------------------------
if __name__ == "__main__":
    main()