import sqlite3
db_name = 'books.db'
#-------------------------------------------------------------
#創建資料表
def sql_create():
    conn = sqlite3.connect(db_name)
    cursor=conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS llm_books
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL UNIQUE,
                      author TEXT,
                      price INTEGER,
                        link TEXT);''')
    conn.commit()
    conn.close()
#-------------------------------------------------------------
#儲存書籍資料
def save_books(books_data:list):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    new_books_count = 0
    for book in books_data:
        #-----------------------------------------------------
        #處理價格欄位確保是整數或None
        price_raw = book.get('price')
        price_db = None
        if isinstance(price_raw, int):
            price_db = price_raw
        #-----------------------------------------------------
        #儲存書籍資料到資料庫
        try:
            cursor.execute('''INSERT INTO llm_books (title, author, price, link)
                              VALUES (?, ?, ?, ?)''',
                           (book.get('title'), 
                            book.get('author', ''), 
                            book.get('price', 0),     
                            book.get('link', ''))) 
        #-----------------------------------------------------
            #計算新增的書籍數量
            if cursor.rowcount > 0:
                new_books_count += 1
        except sqlite3.IntegrityError:
            print(f"書籍已存在，跳過: {book['title']}")
        except Exception as e:
            print(f"儲存書籍時發生錯誤: {e}")
    conn.commit()
    conn.close()
    return new_books_count
#-------------------------------------------------------------

'''if __name__ == "__main__":
    print("--- 正在單獨測試 database.py ---")
    sql_create()
    # 修正 print 訊息中的資料表名稱
    print(f"資料庫 '{db_name}' 和 'llm_books' 資料表已確認。")
    
    # 1. 模擬爬蟲抓到的真實資料 (包含 N/A 情況)
    test_data = [
        {'title': '測試書本A (新書)', 'author': '作者A', 'price': 500, 'link': 'http://link.A'},
        {'title': '測試書本B (N/A價)', 'author': '作者B', 'price': 'N/A', 'link': 'http://link.B'},
        {'title': '測試書本C (無價格)', 'author': '作者C', 'price': None, 'link': 'http://link.C'}
    ]
    print(f"\n--- 第一次存入 {len(test_data)} 筆 (含 N/A 價格) ---")
    count1 = save_books(test_data)
    print(f"第一次存入: {count1} 筆新資料") # 應為 3
    
    # 2. 模擬第二次執行, 包含重複資料
    test_data_2 = [
        {'title': '測試書B-n本A (新書)', 'author': '作者A', 'price': 500, 'link': 'http://link.A'}, # 這是重複的
        {'title': '測試書本D (新書)', 'author': '作者D', 'price': 123, 'link': 'http://link.D'}
    ]
    print(f"\n--- 第二次存入 {len(test_data_2)} 筆 (含重複資料) ---")
    count2 = save_books(test_data_2)
    print(f"第二次存入: {count2} 筆新資料") # 應為 1'''