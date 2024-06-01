import sqlite3
import os
import json
import csv
import re

def create_database():
    # 判斷資料庫檔是否存在
    if not os.path.exists('library.db'):
        try:
            with sqlite3.connect('library.db') as conn:
                cursor = conn.cursor()
                # 建立 users 資料表
                cursor.execute('''CREATE TABLE users (
                                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    username TEXT NOT NULL,
                                    password TEXT NOT NULL
                                )''')

                # 建立 books 資料表
                cursor.execute('''CREATE TABLE books (
                                    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    title TEXT NOT NULL,
                                    author TEXT  NULL,
                                    publisher TEXT  NULL,
                                    year INTEGER  NULL
                                )''')
                conn.commit()
                return True
        except sqlite3.Error as es:
        # 新增圖書資料時發生錯誤
             raise sqlite3.Error(f"新增圖書資料時發生錯誤: {es}")
        except Exception as e:
            raise Exception(f"其他錯誤: {e}")

def datain():
    try:
        # 從檔案讀取並插入使用者資料
        with open(r'.\csv\users.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
        users = [(row['username'], row['password']) for row in reader]
        insert_users(users)
        # 從檔案讀取並插入圖書資料
        with open(r'.\json\books.json', 'r', encoding='utf-8') as f:
            books = json.load(f)
        books = [(book['title'], book['author'], book['publisher'], book['year']) for book in books]
        insert_books(books)

    except csv.Error as e:
        raise csv.Error(f"讀取CSV發生錯誤: {e}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"讀取JSON發生錯誤: {e}")
    except Exception as e:
        raise Exception(f"其他錯誤: {e}")

def insert_users(users:dict):
    """依user.csv新增資料"""
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.executemany("INSERT INTO users (username, password) VALUES (?, ?)", users)
            conn.commit()
    except sqlite3.Error as e:
        raise sqlite3.Error (f"新增使用者資料時發生錯誤: {e}")
    except Exception as e:
            raise Exception(f"其他錯誤: {e}")

def insert_books(books:dict):
    """依books.json新增book資料"""
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.executemany("INSERT INTO books (title, author, publisher, year) VALUES (?, ?, ?, ?)", books)
            conn.commit()
            return True
    except sqlite3.Error as e:
        raise sqlite3.Error (f"新增圖書資料時發生錯誤: {e}")
    except Exception as e:
            raise Exception(f"其他錯誤: {e}")


def login(username:str, password:str):
    """檢查LOGOIN資料正確否 傳回 user"""
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            return user
    except sqlite3.Error as e:
        raise sqlite3.Error (f"輸入資料不正確: {e}")
    except Exception as e:
            raise Exception(f"其他錯誤: {e}")


def show_menu():
    """選單目錄和並選擇
       練習 print *
    """
    print("-"*19)
    print(" 資料表 CRUD")
    print("-"*19)
    print(" 1. 增加記錄")
    print(" 2. 刪除記錄")
    print(" 3. 修改記錄")
    print(" 4. 查詢記錄")
    print(" 5. 資料清單")
    print("-"*19)
    choice = input("選擇要執行的功能(Enter離開)：")
    return choice

def add_record():
    """
    新增書本
    練習  try:
          except
    """
    title = input("請輸入要新增的標題：")
    author = input("請輸入要新增的作者：")
    publisher = input("請輸入要新增的出版社：")
    year = input("請輸入要新增的年份：")
    if title and author and publisher and year:
        try:
            year = int(year)
            ck=insert_books([(title, author, publisher, year)])
            if ck:
                return True
        except ValueError as e:
             raise ValueError (f"年份必須是數字。{e}")
        except Exception as e:
            raise Exception(f"其他錯誤: {e}")

    else:
        raise ValueError ("給定的條件不足，無法進行新增作業")




def delete_record():
    """
    依書名刪除資料
    """
    title = input("請問要刪除哪一本書？：")
    if title:
        try:
            with sqlite3.connect('library.db') as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM books WHERE title=?", (title,))
                conn.commit()
                return True
        except sqlite3.Error as e:
             raise sqlite3.Error (f"給定的條件不足，無法進行刪除作業: {e}")
        except Exception as e:
            raise Exception(f"其他錯誤: {e}")
    else:
       raise ValueError (f"給定的條件不足，無法進行刪除作業")

def update_record():
    """
    依書名更新資料
    """
    title = input("請問要修改哪一本書的標題？：")
    new_title = input("請輸入要更改的標題：")
    new_author = input("請輸入要更改的作者：")
    new_publisher = input("請輸入要更改的出版社：")
    new_year = input("請輸入要更改的年份：")
    if new_title and new_author and new_publisher and new_year:
        try:
            new_year = int(new_year)
            with sqlite3.connect('library.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''UPDATE books SET title=?, author=?, publisher=?, year=?
                                WHERE title=?''', (new_title, new_author, new_publisher, new_year, title))
                conn.commit()
                return True
        except ValueError as ve:
            raise ValueError (f"年份必須是數字。{ve}")
        except sqlite3.Error as se:
            raise sqlite3.Error (f"資料庫錯誤：{se}")
        except Exception as e:
            raise Exception(f"其他錯誤: {e}")
    else:
         raise ValueError ("給定的條件不足，無法進行修改作業")

def error_print():
    """
    如果有錯時列印 錯誤資訊
    """

def search_record():
    """
    依書名查詢資料
    """
    keyword = input("請輸入想查詢的關鍵字：")
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT title, author, publisher, year FROM books
                            WHERE title LIKE ? OR author LIKE ?''', ('%' + keyword + '%', '%' + keyword + '%'))
            results = cursor.fetchall()
            print_date(results)
    # except sqlite3.Error as e:
    #     print(f"輸入資料不正確: {e}")
    except sqlite3.Error as se:
        raise sqlite3.Error (f"輸入資料不正確: {se}")
    except Exception as e:
        raise Exception(f"其他錯誤: {e}")


def list_records():
    """查所有書本"""
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title, author, publisher, year FROM books")
            results = cursor.fetchall()
            print_date(results)
    except sqlite3.Error as se:
        raise sqlite3.Error (f"輸入資料不正確: {se}")
    except Exception as e:
        raise Exception(f"其他錯誤: {e}")


def pad_to_width(word:str, width:int, )->str:
    """
    補字元使的 width 符合設定
    因半形字與全形字的不同寬

    """
    s = str(word)
    half_width_count = len(re.findall(r'[\x00-\x7F]', s))  # 找出半形字的數量
    full_width_count = len(s) - half_width_count  # 找出全形字的數量

    s_width = width -len(s)   # 計算無半型字串要補的的空白
    padding = width -full_width_count-(half_width_count//2) # 計算有半形的需要填充的空格數量

    if half_width_count  > 0:                    #如果有半形字
        if half_width_count %2==0:                   #如果半形字為偶數
            return s + chr(12288) * padding              # 填充全形空白
        else:                                        #如果半形字為奇數
            padding=padding-1
            return s+ chr(12288) * padding +' '         # 填充全形空白+一個空格 chr(32)
    return s+ chr(12288) *(s_width)               #如果沒有半形字


def print_date(data: dict):
    """輸出結果  進行補空白對齊"""
    col_width=[10, 12, 18, 4] #這定欄寬
    header= ["書名", "作者", "出版社", "年份"]
    # print(f"|{'書名':{chr(12288)}^{col_width[0]}}|{'作者':{chr(12288)}^{col_width[1]}}|{'出版社':{chr(12288)}^{col_width[2]}}|{'年份':{chr(12288)}^{col_width[3]}}|")
    #改列表推導式
    print_data=f"|"+"|".join(f'{col:{chr(12288)}^{width}}' for col, width in zip(header,col_width))+"|"
    print(print_data)


    for row in data:
        # spvalue0 = pad_to_width(row[0],col_width[0])
        # spvalue1 = pad_to_width(row[1],col_width[1])
        # spvalue2 = pad_to_width(row[2],col_width[2])
        # spvalue3 = pad_to_width(row[3],col_width[3])
        # print(f"|{spvalue0}|{spvalue1}|{spvalue2}|{spvalue3}|")
        print_data="| "+ " | ".join(pad_to_width(col, width) for col, width in zip(row, col_width))+ " |"
        # formatted_row = "| " + " | ".join(pad_to_width(col, width) for col, width in zip(row, col_width)) + " |"
        print(print_data)



