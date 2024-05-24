import os
import sqlite3
import json
import pandas as pd

def config_load(config_file):
    '''加载 JSON 配置文件'''
    with open(config_file, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

def create_table(conn, create_table_sql):
    '''创建表格'''
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except sqlite3.Error as e:
        print(f"創建資料表錯了: {e}")

def create_db(config):
    '''根据 JSON 配置文件創建資料表'''
    dp_name = config.get("dp_name", library.db)
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

def date_load(table_name, config):

    dp_name = config.get("dp_name", "library.db")
    table_config = next((table for table in config["tables"] if table["table_name"] == table_name), None)
    if not table_config:
        raise ValueError(f"表 {table_name} 在配置文件中未找到")

    columns = table_config["select_columns"]
    columns_str = ', '.join(columns)
    sql = f"select ({columns_str}) from {table_name}"

    try:
        with sqlite3.connect(dp_name) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            # 列印查詢結果的標題
            print("查詢結果：")
            header = "| " + " | ".join(columns) + " |"
            print("-" * len(header))
            print(header)
            print("-" * len(header))
            # 列印查詢結果的數據
            for row in rows:
                row_str = "| " + " | ".join(str(col) for col in row) + " |"
                print(row_str)

            print("-" * len(header))
          # cursor.execute(f"SELECT 1 FROM {table_name} WHERE {pk_conditions}", pk_values)
    except sqlite3.Error as error:
        print(f" 作業發生错误：{error}")



