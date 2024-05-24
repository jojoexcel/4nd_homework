import sqlite3
import pack.modu as lib


def date_load(table_name, data, config):
    # 從配置文件中獲取數據庫名稱
    # dp_name = config.get("dp_name", "library.db")

    # # 獲取指定表格的配置信息
    # table_config = next((table for table in config["tables"] if table["table_name"] == table_name), None)
    # if not table_config:
    #     raise ValueError(f"表 {table_name} 在配置文件中未找到")

    # # 獲取表格的欄位名稱
    # columns = table_config["select_columns"]
    # columns_str = ', '.join(columns)

    sql = f"SELECT * FROM books "
    try:
        # 連接數據庫
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            result_all = cursor.fetchall()
            print_records(result_all)
    except sqlite3.Error as error:
            print(f"作業發生錯誤：{error}")
            print(f"{columns_str}")

def print_records(records):
    if records:
        print(f"|{'書名':{chr(12288)}^12}|{'作者':{chr(12288)}^12}|{'出版社':{chr(12288)}^12}|{'年份':^4}|")
        for row in records:
            print(f"|{row[0]:{chr(12288)}<12}|{row[1]:{chr(12288)}<12}|{row[2]:{chr(12288)}<12}|{row[3]:<6}|")
    else:
        print("無相符記錄")

DB_config_file = r'.\json\db_config.json'
config = lib.config_load(DB_config_file)
lib.date_load('books', config)
