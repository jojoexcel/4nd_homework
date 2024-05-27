import os
import sqlite3
import pandas as pd
import json
import pack.modu as lib
# 需在外層才能作用
DB_config_file = r'.\json\db_config.json'
config = lib.config_load(DB_config_file)
# 測試插入單個用戶
user_data = {'username': 'testuser12', 'password': 'd124'}
lib.insert_user('users', user_data, config)

# # 測試插入單本書
book_data = {'title': 'Example Book02', 'author': 'John Doe2', 'publisher': 'Example Publisher', 'year': 2024}
lib.insert_user('books', book_data, config)

# -----LOAD
DB_config_file = r'.\json\db_config.json'
config = lib.config_load(DB_config_file)
table="books"
lib.date_load(table, config)

# def date_load(table_name, config, column_names):
    # dp_name = config.get("dp_name", "library.db")
    # table_config = next((table for table in config["tables"] if table["table_name"] == table_name), None)
    # if not table_config:
    #     raise ValueError(f"表 {table_name} 在配置文件中未找到")

    # if column_names not in table_config:
    #     raise ValueError(f"列名 {column_names} 在表 {table_name} 的配置中未找到")

    # # columns = table_config[column_names]  單一json

    # columns = [col["name"] for col in table_config[column_names]]  # 雙層取得

    # columns_str = ', '.join(columns)
    # sql = f"SELECT {columns_str} FROM {table_name} "

    # try:
    #     with sqlite3.connect(dp_name) as conn:
    #         cursor = conn.cursor()
    #         cursor.execute(sql)
    #         all_data = cursor.fetchall()
    #         clear_screen()
    #         print_records(all_data, columns)
    #         display_menu()
    # except sqlite3.Error as error:
    #     print(f" 作業發生错误：{error}")

# def print_records(records, column_names):
#     if records:
#         print(f"|{'NO':{chr(32)}^4}|{'書名':{chr(12288)}^12}|{'作者':{chr(12288)}^12}|{'出版社':{chr(12288)}^8}|{'年份':{chr(12288)}^4}|")
#         for row in records:
#             print(f"|{row[0]:{chr(32)}^4}|{row[1]:{chr(12288)}<12}|{row[2]:{chr(12288)}<12}|{row[3]:{chr(12288)}<8}|{row[4]:{chr(12288)}^6}|")
#     else:
#         print("無相符記錄")


# def print_records(records, column_names):
#     if records:
#         header = "| " + " | ".join(f'{name:{chr(12288)}^10}' for name in column_names) + " |"
#         print("-" * len(header))
#         print(header)
#         print("-" * len(header))
#         for row in records:
#             formatted_row = "| " + " | ".join(f'{str(col):{chr(12288)}^10}' for col in row) + " |"
#             print(formatted_row)
#         print("-" * len(header))
#     else:
#         print("無相符記錄")