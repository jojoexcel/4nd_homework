import os
import sqlite3
import json
import pandas as pd


def config_load(config_file):
    '''加载 JSON 配置文件'''
    with open(config_file, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_table(conn, create_table_sql):
    '''创建表格'''
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except sqlite3.Error as e:
        print(f"創建資料表錯了: {e}")

def create_db(config):
    '''根据 JSON 配置文件創建資料表'''
    dp_name = config.get("dp_name", "library.db")
    tables = config.get("tables", [])
    conn = sqlite3.connect(dp_name)
    for table_config in tables:
        create_table(conn, table_config['create_table'])

    conn.commit()
    conn.close()

def insert_users_from_file(file, table_name, config):
    '''根據文件批量插入資料'''
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
        raise ValueError("不支持的文件，只支持 CSV, JSON 和 Excel (XLSX, XLS) 文件")

    data = df.to_dict(orient='records')
    insert_data(table_name, data, config)


def insert_data(table_name, data, config):
    '''批量插入数据'''
    dp_name = config.get("dp_name", "library.db")
    table_config = next((table for table in config["tables"] if table["table_name"] == table_name), None)

    if not table_config:
        raise ValueError(f"表 {table_name} 在配置文件中未找到")

    columns = table_config["insert_columns"]
    primary_key = table_config.get("primary_key", [])
    placeholders = ', '.join(['?'] * len(columns))
    columns_str = ', '.join(columns)

    sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

    try:
        with sqlite3.connect(dp_name) as conn:
            cursor = conn.cursor()
            for row in data:
                # 检查主键是否存在
                if primary_key:
                    pk_values = [row[pk] for pk in primary_key]
                    pk_conditions = ' AND '.join([f"{pk} = ?" for pk in primary_key])
                    cursor.execute(f"SELECT 1 FROM {table_name} WHERE {pk_conditions}", pk_values)
                    if cursor.fetchone():
                        print(f"新增失敗,資料重覆了{primary_key}  {pk_values}")
                        continue

                values = [row[col] for col in columns]
                cursor.execute(sql, values)
            conn.commit()
    except sqlite3.Error as error:
        print(f"新增数据时发生错误：{error}")

def insert_user(table_name, data, config):
    '''插入單一資料'''
    dp_name = config.get("dp_name", "library.db")  # 使用配置文件中的数据库名称

    table_config = next((table for table in config["tables"] if table["table_name"] == table_name), None)
    if not table_config:
        raise ValueError(f"表 {table_name} 在配置文件中未找到")

    columns = table_config["insert_columns"]
    primary_key = table_config.get("primary_key", [])
    placeholders = ', '.join(['?'] * len(columns))
    columns_str = ', '.join(columns)

    sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

    values = [data[col] for col in columns]

    try:
        with sqlite3.connect(dp_name) as conn:
            cursor = conn.cursor()
            # 检查主键是否存在
            if primary_key:
                pk_values = [data[pk] for pk in primary_key]
                pk_conditions = ' AND '.join([f"{pk} = ?" for pk in primary_key])
                cursor.execute(f"SELECT 1 FROM {table_name} WHERE {pk_conditions}", pk_values)
                if cursor.fetchone():
                   hi = f"{table_name}新增失敗,\n欄位:{primary_key} \n資料:{pk_values}\n重複了"
                   print(f"{hi:<10}")
                   return

            cursor.execute(sql, values)
            conn.commit()
    except sqlite3.Error as error:
        print(f"新增 {table_name} 作業發生错误：{error}")

def date_load(table_name, config, fun_json):
    dp_name = config.get("dp_name", "library.db")
    table_config = next((table for table in config["tables"] if table["table_name"] == table_name), None)
    if not table_config:
        raise ValueError(f"表 {table_name} 在配置文件中未找到")

    columns = [col["name"] for col in table_config[fun_json]]
    # columns_h=[col["description"] for col in table_config[fun_json]]
    # columns_w=[col["with"] for col in table_config[fun_json]]
    columns_str = ', '.join(columns)
    sql = f"SELECT {columns_str} FROM {table_name} "

    try:
        with sqlite3.connect(dp_name) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            all_data = cursor.fetchall()
            clear_screen()
            print_records(all_data, columns, table_config ,fun_json)
            display_menu()
    except sqlite3.Error as error:
        print(f" 作業發生错误：{error}")

def print_records(all_data, columns, table_config, fun_json):
    if all_data:
        header = "| " + " | ".join(f'{col["description"]:{chr(12288)}^{col["width"]}}' for col in table_config[fun_json]) + " |"
        # print("-" * len(header))
        print(header)
        # print("-" * len(header))
        for row in all_data:
            if len(row) == len(columns):
                formatted_row = "| " + " | ".join(f'{str(col):{chr(12288)}^{col_settings["width"]}}' for col, col_settings in zip(row, table_config[fun_json])) + " |"
                print(formatted_row)
            else:
                print("資料欄位數量與設定不符")
        # print("-" * len(header))
    else:
        print("無相符記錄")

def check_user():
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

def select_books_like_title_or_author(dp_name, table_name, config, fun_json):
    table_config = next((table for table in config["tables"] if table["table_name"] == table_name), None)
    if not table_config:
        raise ValueError(f"表 {table_name} 在配置文件中未找到")
    columns = [col["name"] for col in table_config[fun_json]]
    columns_str = ', '.join(columns)
    columns_where = table_config["select_where_columns"]
    columns_where_str = ' OR '.join(f"{col} LIKE ?" for col in columns_where)

    try:
        keyword = input('請輸入書名或作者關鍵字:')

        with sqlite3.connect(dp_name) as conn:
            cursor = conn.cursor()
            sql = f"SELECT {columns_str} FROM {table_name} WHERE {columns_where_str}"
            cursor.execute(sql, ('%'+keyword+'%', '%'+keyword+'%'))
            all_data = cursor.fetchall()

            if all_data:
                clear_screen()
                print_records(all_data, columns, table_config ,fun_json)
                display_menu()
            else:
                print("無相符記錄")
    except sqlite3.Error as error:
        print(f"查詢作業發生錯誤：{error}")

def display_menu():
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
    DB_config_file = r'.\json\db_config.json'
    config = config_load(DB_config_file)
    table="books"
    fun_json="select_columns"
    date_load(table, config, fun_json)

