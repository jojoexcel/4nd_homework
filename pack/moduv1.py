import os
import sqlite3
import json
import pandas as pd
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

DB_config_file='db_config.json'
config = config_load(DB_config_file)
conn = create_db(config)
conn.close()

# json_data='DB_config.json'
# config = config_load(json_data)
# create_db(config)