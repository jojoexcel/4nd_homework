import sqlite3
import json
import os
from math import ceil


def config_load(config_file: str) -> dict:
    '''載入 JSON 參數。

    Args:
        config_file (str): JSON 配置文件的路徑。

    Returns:
        dict: 從 JSON 文件中載入的配置。
    '''
    with open(config_file, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config
# def clear_screen():
#     os.system('cls' if os.name == 'nt' else 'clear')

def create_db(config):
    '''
    根據 JSON 配置文件創建資料表

    Args:
        config (dict): JSON 配置字典，包含資料庫名稱（dp_name）和資料表資訊（tables）。

    Returns:
        None

    Raises:
        sqlite3.Error: 創建資料表時發生的錯誤。
    '''
    dp_name = config.get("dp_name", "library.db")
    tables = config.get("tables", [])

    try:
        with sqlite3.connect(dp_name) as conn:
            for table_config in tables:
                create_table(conn, table_config['create_table'])
            conn.commit()
    except sqlite3.Error as e:
        print(f"創建資料表錯了: {e}")

def create_table(conn, create_table_sql):
    '''
    創建資料表

    Args:
        conn (sqlite3.Connection): SQLite 連接物件。
        create_table_sql (str): 創建資料表的 SQL 語句。

    Returns:
        None

    Raises:
        sqlite3.Error: 創建資料表時發生的錯誤。
    '''
    try:
        with conn:
            conn.execute(create_table_sql)
    except sqlite3.Error as e:
        print(f"創建資料表錯了: {e}")

def insert_users_from_file(file: str, table_name: str, config: dict):
    '''根據檔案批次插入資料'''
    ext = os.path.splitext(file)[1].lower()
    if ext == '.csv':
        data = read_csv(file)
    elif ext == '.json':
        data = read_json(file)
    else:
        raise ValueError("資料格式只支援 CSV 和 JSON 檔案")

    insert_data(table_name, data, config)

def read_csv(file: str) -> list:
    '''讀取 CSV 檔案並返回資料'''
    data = []
    with open(file, 'r', encoding='utf-8') as f:
        headers = f.readline().strip().split(',')
        for line in f:
            values = line.strip().split(',')
            record = dict(zip(headers, values))
            data.append(record)
    return data

def read_json(file: str) -> dict:
    '''讀取 JSON 檔案並返回資料'''
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def insert_data(table_name: str, data: list, config: dict):
    '''批次插入資料'''
    dp_name = config.get("dp_name", "library.db")
    table_config = next((table for table in config["tables"] if table["table_name"] == table_name), None)

    if not table_config:
        raise ValueError(f"表格 {table_name} 在配置文件中未找到")

    columns = table_config["insert_columns"]
    primary_key = table_config.get("primary_key", [])
    placeholders = ', '.join(['?'] * len(columns))
    columns_str = ', '.join(columns)

    sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

    try:
        with sqlite3.connect(dp_name) as conn:
            cursor = conn.cursor()
            for row in data:
                # 檢查主鍵是否存在
                if primary_key:
                    pk_values = [row[pk] for pk in primary_key]
                    pk_conditions = ' AND '.join([f"{pk} = ?" for pk in primary_key])
                    cursor.execute(f"SELECT 1 FROM {table_name} WHERE {pk_conditions}", pk_values)
                    if cursor.fetchone():
                        print(f"新增失敗，資料重覆了 {primary_key} {pk_values}")
                        continue

                values = [row[col] for col in columns]
                cursor.execute(sql, values)
            conn.commit()
    except sqlite3.Error as error:
        print(f"新增資料時發生錯誤：{error}")

def data_insert(table_name: str, config: dict, fun_json: str):
    '''插入單一資料'''
    dp_name = config.get("dp_name", "library.db")
    table_config = next((table for table in config["tables"] if table["table_name"] == table_name), None)
    if not table_config:
        raise ValueError(f"表 {table_name} 在配置文件中未找到")

    columns = table_config[fun_json]
    columns_name_tw = [next(col["description"] for col in table_config["columns_set"] if col["name"] == column) for column in columns]
    # columns_name_why = [next(col["why"] for col in table_config["columns_set"] if col["name"] == column) for column in columns]
    primary_key = table_config.get("primary_key", [])
    placeholders = ', '.join(['?'] * len(columns))
    columns_str = ', '.join(columns)

    sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
    """ 一有錯就停
    values = []
    for i, col in enumerate(columns):
        value = input(f'{columns_name_why[i]}：').strip()
        if not value:
            print(f'給定的條件不足，無法進行新增作業')
            return False
        values.append(value)
    """
    """ 直到正確
    values = []
    for i, col in enumerate(columns):
        while True:
            value = input(f'{columns_name_why[i]}：').strip()
            if value:
                values.append(value)
                break
            else:
                print("输入不能为空，请重新输入。")

    """
    """全部打完才檢查"""
    values = []
    for i, col in enumerate(columns):
        value = input(f'請輸入要新增的{columns_name_tw[i]}：').strip()
        values.append(value)

    if check_empty_values(values):
        print(f'給定的條件不足，無法進行新增作業')
        return False

    try:
        with sqlite3.connect(dp_name) as conn:
            cursor = conn.cursor()
            # 检查主键是否存在
            if primary_key:
                pk_values = [values[columns.index(pk)] for pk in primary_key]
                pk_conditions = ' AND '.join([f"{pk} = ?" for pk in primary_key])
                cursor.execute(f"SELECT 1 FROM {table_name} WHERE {pk_conditions}", pk_values)
                if cursor.fetchone():
                    print(f"新增失敗，書本已存在")
                    return False

            cursor.execute(sql, values)
            cursor_ros=cursor.rowcount
            conn.commit()
            # select_books_all()
            return cursor_ros
            # display_menu()

    except sqlite3.Error as error:
        print(f"新增 {table_name} 作業發生错误：{error}")

def check_empty_values(lst):
    return any(not item for item in lst)

def date_update_chack_name(book_name: str, config: dict, table_name: str):
    dp_name = config.get("dp_name", "library.db")
    try:
        with sqlite3.connect(dp_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT title FROM {table_name} WHERE title = ?", (book_name,))
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False
    except sqlite3.Error as error:
        print(f"查詢書名時發生錯誤：{error}")
        return False

def data_update(table_name: str, config: dict, fun_json: str):
    dp_name = config.get("dp_name", "library.db")
    table_config = next((table for table in config["tables"] if table["table_name"] == table_name), None)
    if not table_config:
        raise ValueError(f"表 {table_name} 在配置文件中未找到")

    update_columns = table_config.get(fun_json, [])
    columns_set = table_config.get("columns_set", [])

    book_name = input('請問要修改哪一本書的標題？：').strip()

    set_clause = ', '.join([f"{col} = ?" for col in update_columns])
    update_values = []

    for col in update_columns:
        col_description = next((c["description"] for c in columns_set if c["name"] == col), col)
        col_value = input(f'請輸入要修改的 {col_description}：').strip()
        update_values.append(col_value)

    if not date_update_chack_name(book_name, config, table_name):
        print(f"書本不存在，無法進行修改作業")
        return False

    if check_empty_values( update_values ):
        print(f'給定的條件不足，無法進行新增作業')
        return False

    try:
        with sqlite3.connect(dp_name) as conn:
            cursor = conn.cursor()
            sql = f"UPDATE {table_name} SET {set_clause} WHERE title = ?"
            cursor.execute(sql, update_values + [book_name])
            cursor_ros=cursor.rowcount
            conn.commit()
            return cursor_ros
            # clear_screen()
            # display_menu()
            # print(f"更新{update_values}成功")

    except sqlite3.Error as error:
        print(f"更新 {table_name} 作業發生錯誤：{error}")

def data_delete(table_name: str, config: dict, fun_json: str):
    dp_name = config.get("dp_name", "library.db")
    table_config = next((table for table in config["tables"] if table["table_name"] == table_name), None)
    if not table_config:
        raise ValueError(f"表 {table_name} 在配置文件中未找到")

    book_name = input('請問要刪除哪一本書？').strip()
    if not date_update_chack_name(book_name, config, table_name):
        print(f"給定的條件不足，無法進行刪除作業")
        return False

    try:
        with sqlite3.connect(dp_name) as conn:
            cursor = conn.cursor()
            sql = f"DELETE FROM {table_name} WHERE title = ?"
            cursor.execute(sql, (book_name,))
            cursor_ros=cursor.rowcount
            conn.commit()
            return cursor_ros
            # clear_screen()
            # display_menu()
            # print(f"書名 '{book_name}' 的記錄已刪除")
    except sqlite3.Error as error:
        print(f"刪除 {table_name} 記錄時發生錯誤：{error}")

def date_load(table_name: str, config: dict, fun_json: str):
    dp_name = config.get("dp_name", "library.db")
    table_config = next((table for table in config["tables"] if table["table_name"] == table_name), None)
    if not table_config:
        raise ValueError(f"表 {table_name} 在配置文件中未找到")

    columns = table_config[fun_json]
    columns_name_tw = [next(col["description"] for col in table_config["columns_set"] if col["name"] == column) for column in columns]
    columns_str = ', '.join(columns)
    sql = f"SELECT {columns_str} FROM {table_name}"

    try:
        with sqlite3.connect(dp_name) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            all_data = cursor.fetchall()
            # clear_screen()
            print_records(all_data,columns_name_tw,table_config,columns)
            # display_menu()
    except sqlite3.Error as error:
        print(f"查詢 {table_name} 作業發生错误：{error}")

def pad_to_width(s: str, width: int) -> str:
    """填充字符串以達到指定寬度，考慮到全角字符

    Args:
        s (str): 要填充的字符串
        width (int): 目標寬度

    Returns:
        str: 填充後的字符串
    """
    s = str(s)
    s_width = sum(2 if ord(char) > 127 else 1 for char in s)  # 計算字符串的顯示寬度
    padding = width - s_width  # 計算需要填充的空格數量

    if padding > 0:
        if padding % 2 == 0:
            return s + chr(12288) * (padding // 2)
        else:
            return s + chr(12288) * (padding // 2) + ' '
    return s  # 如果不需要填充，返回原字符串

def print_records(all_data, columns_name_tw, table_config, columns):
    """打印記錄

    Args:
        all_data (list): 所有要打印的記錄
        columns_name_tw (list): 中文列名列表
        table_config (dict): 表格配置信息
        columns (list): 列名列表
    """
    if all_data:
        # 打印表頭
        # header = "| " + " | ".join(pad_to_width(col, col_with["width"]) for col, col_with in zip(columns_name_tw, table_config["columns_set"])) + " |"
        # print(header)
        print(f"|{'書名':{chr(12288)}^7}|{'作者':{chr(12288)}^7}|{'出版社':{chr(12288)}^10}|{'年份':^4}|")
        # # 打印分隔線--加這個不錯看
        # separator = "|-" + "-|-".join("-" * col_with["width"] for col, col_with in zip(columns_name_tw, table_config["columns_set"])) + " |"
        # print(separator)
        # 打印每一行數據
        for row in all_data:
            if len(row) == len(columns):
                formatted_row = "| " + " | ".join(pad_to_width(str(col), col_settings["width"]) if col_settings["name"] in columns else pad_to_width(str(col), col_settings["width"]) for col, col_settings in zip(row, table_config["columns_set"])) + " |"
                print(formatted_row)
            else:
                print("資料欄位數量與設定不符")

    else:
        print("無相符記錄")


def check_user() -> str:
    """檢查用戶

    Returns:
        str: 登入結果
    """
    dp_name = 'library.db'
    table_name = "users"

    try:
        username = input('請輸入帳號：')
        password = input('請輸入密碼：')

        with sqlite3.connect(dp_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT password FROM {table_name} WHERE username = ?", (username,))
            result = cursor.fetchone()

            if result:
                stored_password = result[0]
                if password == stored_password:
                    return "登入成功"
                else:
                    return "密碼錯誤"
            else:
                return "用戶不存在！"

    except sqlite3.Error as error:
        print(f"查詢作業發生錯誤：{error}")


def select_books_like_title_or_author(table_name: str, config: dict, fun_json: str) -> bool:
    """根據書名或作者關鍵字選擇書籍

    Args:
        table_name (str): 表名
        config (dict): 配置信息
        fun_json (str): 函數 JSON

    Returns:
        bool: 是否成功查詢到記錄
    """
    # select_books_like_title_or_author(db_path, table_name, config, fun_json)
    dp_name = config.get("dp_name", "library.db")
    table_config = next((table for table in config["tables"] if table["table_name"] == table_name), None)
    if not table_config:
        raise ValueError(f"表 {table_name} 在配置文件中未找到")

    columns = table_config[fun_json]
    columns_str = ', '.join(columns)
    columns_where = table_config["select_where_columns"]
    columns_where_str = ' OR '.join(f"{col} LIKE ?" for col in columns_where)

    try:
        keyword = input('請輸入書名或作者關鍵字:').strip()

        with sqlite3.connect(dp_name) as conn:
            cursor = conn.cursor()
            sql = f"SELECT {columns_str} FROM {table_name} WHERE {columns_where_str}"
            cursor.execute(sql, tuple(f'%{keyword}%' for _ in columns_where))
            all_data = cursor.fetchall()

            if all_data:
                # clear_screen()
                columns_name_tw = [next(col["description"] for col in table_config["columns_set"] if col["name"] == column) for column in columns]
                print_records(all_data,columns_name_tw,table_config,columns)
                return True
                # display_menu()
            else:
                print("無相符記錄")
    except sqlite3.Error as error:
        print(f"查詢作業發生錯誤：{error}")


def display_menu():
    """顯示菜單"""
    print("")
    print(f"{'-'*19}")
    print(f"{'資料表 CRUD':{chr(12288)}^12}")
    print(f"{'-'*19}")
    print(f"{'1. 增加記錄':{chr(12288)}^12}")
    print(f"{'2. 刪除記錄':{chr(12288)}^12}")
    print(f"{'3. 修改記錄':{chr(12288)}^12}")
    print(f"{'4. 查詢記錄':{chr(12288)}^12}")
    print(f"{'5. 資料清單':{chr(12288)}^12}")
    print(f"{'-'*19}")

def select_books_all():
    """讀取所有書本資料"""
    DB_config_file = r'.\json\db_config.json'
    config = config_load(DB_config_file)
    table = "books"
    fun_json = "select_columns"
    date_load(table, config, fun_json)
