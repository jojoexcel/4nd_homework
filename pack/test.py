import pandas as pd
import os
import sqlite3
from tkinter import Tk, filedialog

def insert_users_from_file(file):
    '''从文件中批量插入 users 数据，根据文件扩展名选择处理方法'''
    ext = os.path.splitext(file)[1].lower()  # 获取文件扩展名并转换为小写

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
        raise ValueError("不支持的文件类型，仅支持 CSV, JSON 和 Excel (XLSX, XLS) 文件")

    users = df.to_dict(orient='records')
    insert_users(users)

def insert_users(users):
    '''批量插入 users 数据'''
    dp_name = 'library.db'  # 数据库名称
    conn = sqlite3.connect(dp_name)
    cursor = conn.cursor()

    for user in users:
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                           (user['username'], user['password']))
        except sqlite3.IntegrityError:
            print(f"用户名 '{user['username']}' 已存在，跳过该记录。")

    conn.commit()
    conn.close()

def select_file_and_insert_users():
    '''显示文件选择对话框并处理文件'''
    Tk().withdraw()  # 隐藏根窗口
    file_path = filedialog.askopenfilename(
        title="选择文件",
        filetypes=(
            ("CSV Files", "*.csv"),
            ("JSON Files", "*.json"),
            ("Excel Files", "*.xlsx;*.xls")
        )
    )

    if file_path:
        try:
            insert_users_from_file(file_path)
            print(f"文件 {file_path} 的数据已成功插入到数据库。")
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")

# 调用函数显示文件选择对话框并插入数据
select_file_and_insert_users()
