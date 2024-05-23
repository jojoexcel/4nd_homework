import os
import sqlite3
import json
import pandas as pd

dp_name='library.db'

def create_db():

    conn = sqlite3.connect(dp_name)
    create_table_users='''
    CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
    )'''

    create_table_books='''
    CREATE TABLE IF NOT EXISTS books (
    book_id	 INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    publisher TEXT NOT NULL,
    year INTEGER NOT NULL
    )
    '''
    cursor = conn.cursor()
    cursor.execute(create_table_users)
    cursor.execute(create_table_books)
    conn.commit()
    conn.close()

def insert_users_from_file(file):
    ''''''
    ext = os.path.splitext(file)[1].lower()  #

    if ext == '.csv':
        df = pd.read_csv(file)
    elif ext == '.json':
        df = pd.read_json(file)
    elif ext in ('.xlsx', '.xls'):
        if ext == '.xlsx':
            df = pd.read_excel(file, engine='openpyxl')
        else:
            df = pd.read_excel(file, engine='xlrd')
    else:
        raise ValueError("不支持文件類行，只有支持 CSV, JSON 和 Excel (XLSX,xls) 文件")

    users = df.to_dict(orient='records')
    insert_users(users)

def insert_users(users):
    '''批量插入 users 数据'''
    try:
        dp_name = 'library.db'  # 数据库名称
        conn = sqlite3.connect(dp_name)
        cursor = conn.cursor()

    # 假设 users 表有两列：username 和 password
        for user in users:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                           (user['username'], user['password']))
        conn.commit()
    except sqlite3.Error as error:
        print(f"新增 users 作業發生錯誤：{error}")

    finally:
        conn.close()

def insert_user(username, password):
    '''insert into 資料表 user'''
    try:
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, password))
        conn.commit()
    except sqlite3.Error as error:
        print(f"新增 users 作業發生錯誤：{error}")

    finally:
        conn.close()



