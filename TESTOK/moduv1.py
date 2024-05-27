import os
import sqlite3
import json
import pandas as pd # type: ignore
from tkinter import Tk, filedialog


def config_load(DB_config_file):
    '''加載 JSON 配置文件'''
    with open(DB_config_file, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

def create_table(conn, create_table_sql):
    '''創建表格'''
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except sqlite3.Error as e:
        print(f"創建表格時出錯: {e}")

def create_db(config):
    '''根據 JSON 配置文件創建數據庫表'''
    dp_name = config.get("dp_name", "library.db")
    tables = config.get("tables", [])

    conn = sqlite3.connect(dp_name)
    for table_config in tables:
        create_table_sql = table_config['create_table']
        cursor = conn.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_config['table_name']}'")
        if cursor.fetchone() is None:
            create_table(conn, create_table_sql)

    conn.commit()
    return conn

def read_csv(file):
    return pd.read_csv(file)

def read_json(file):
    return pd.read_json(file)

def read_excel(file):
    ext = os.path.splitext(file)[1].lower()
    if ext == '.xlsx':
        return pd.read_excel(file, engine='openpyxl')
    elif ext == '.xls':
        return pd.read_excel(file, engine='xlrd')
    else:
        raise ValueError("不支持的文件類型，只支持 Excel (XLSX, XLS) 文件")

def insert_users_from_file(file, table_name, config):
    '''根據文件批量插入數據'''
    ext = os.path.splitext(file)[1].lower()

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
        raise ValueError("不支持的文件類型，僅支持 CSV, JSON 和 Excel (XLSX, XLS) 文件")

    data = df.to_dict(orient='records')
    insert_data(table_name, data, config)

def insert_data(table_name, data, config):
    '''批量插入數據'''
    dp_name = config.get("dp_name", "library.db")
    table_config = next((table for table in config["tables"] if table["table_name"] == table_name), None)

    if not table_config:
        raise ValueError(f"表 {table_name} 在配置文件中未找到")

    columns = table_config["insert_columns"]
    placeholders = ', '.join(['?'] * len(columns))
    columns_str = ', '.join(columns)

    sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

    try:
        with sqlite3.connect(dp_name) as conn:
            cursor = conn.cursor()
            for row in data:
                values = [row[col] for col in columns]
                cursor.execute(sql, values)
            conn.commit()
    except sqlite3.Error as error:
        print(f"新增數據時發生錯誤：{error}")

def insert_user(table_name, data, config):
    '''插入單個用戶數據'''
    dp_name = config.get("dp_name", "library.db")  # 使用配置文件中的資料庫名稱

    table_config = next((table for table in config["tables"] if table["table_name"] == table_name), None)
    if not table_config:
        raise ValueError(f"表 {table_name} 在配置文件中未找到")

    columns = table_config["insert_columns"]
    placeholders = ', '.join(['?'] * len(columns))
    columns_str = ', '.join(columns)

    sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
    # 設定要寫入的欄位值  代入新增SQL
    values = [data[col] for col in columns]

    try:
        with sqlite3.connect(dp_name) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, values)
            conn.commit()
    except sqlite3.Error as error:
        print(f"新增 {table_name} 作業發生錯誤：{error}")

# def loaddate():


#----------------------------------------------------------
# def 主程序():
    # '''主程序入口'''
    # # 加載 JSON 配置文件
    # # Tk().withdraw()
    # # DB_config_file = filedialog.askopenfilename(
    # #     title="選擇配置文件",
    # #     filetypes=(
    # #         ("JSON 文件", "*.json"),
    # #     )
    # # )
    # DB_config_file='db_config.json'
    # if DB_config_file:
    #     config = config_load(DB_config_file)
    #     conn = create_db(config)
    #     print(f"根據配置文件 {DB_config_file} 創建數據庫表成功。")
    #     conn.close()

# if __name__ == '__main__':
#     主程序()
#-------------------------------------------
# TEST
# DB_config_file=r'.\json\db_config.json'
# config = config_load(DB_config_file)
# conn = create_db(config)
# conn.close()