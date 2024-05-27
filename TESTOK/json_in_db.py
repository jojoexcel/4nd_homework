import sqlite3
import json

def config_load(config_file):
    '''加载 JSON 配置文件'''
    with open(config_file, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

# 插入配置數據到數據庫
def insert_config():
    config_file=r".\json\DB_config.json"
    config_data=config_load(config_file)
    dp_name = config_data["dp_name"]
    try:
        with sqlite3.connect(dp_name) as conn:
            cursor = conn.cursor()
            # 創建表
            cursor.execute("""
                 CREATE TABLE IF NOT EXISTS table_configs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_name TEXT NOT NULL,
                    description TEXT,
                    create_table TEXT,
                    select_where_columns TEXT,
                    insert_columns TEXT,
                    update_columns TEXT,
                    primary_key TEXT
                )
            """)
            ''' fun_name )
                     table_name ,
                     description ,
                     create_table ,
                     select_where_columns ,
                     insert_columns ,
                     update_columns ,
                     primary_key )
            '''
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS column_configs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_id INTEGER,


                    name TEXT NOT NULL,
                    description TEXT,
                    width INTEGER,
                    FOREIGN KEY(table_id) REFERENCES table_configs(id)
                )
            """)

            for table in config_data["tables"]:
                # 插入 table 配置
                cursor.execute("""
                    INSERT INTO table_configs (table_name, description, create_table, select_where_columns, insert_columns, update_columns, primary_key)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    table["table_name"],
                    table["description"],
                    table["create_table"],
                    json.dumps(table["select_where_columns"]),
                    json.dumps(table["insert_columns"]),
                    json.dumps(table["update_columns"]),
                    json.dumps(table["primary_key"])
                ))
                table_id = cursor.lastrowid

                # 插入 column 配置
                for column in table["select_columns"]:
                    cursor.execute("""
                        INSERT INTO column_configs (table_id, name, description, width)
                        VALUES (?, ?, ?, ?)
                    """, (
                        table_id,
                        column["name"],
                        column["description"],
                        column["width"]
                    ))

            conn.commit()
            print("配置數據插入成功")
    except sqlite3.Error as error:
        print(f"插入配置數據時發生錯誤：{error}")

# 執行插入配置數據
# insert_config()

# 從數據庫讀取配置
def load_config_from_db():
    dp_name = "library.db"
    try:
        with sqlite3.connect(dp_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM table_configs")
            tables = cursor.fetchall()
            config_data = {"dp_name": dp_name, "tables": []}
            for table in tables:
                table_id, table_name, description, create_table, select_where_columns, insert_columns, update_columns, primary_key = table
                cursor.execute("SELECT name, description, width FROM column_configs WHERE table_id=?", (table_id,))
                columns = cursor.fetchall()
                table_dict = {
                    "table_name": table_name,
                    "description": description,
                    "create_table": create_table,
                    "select_columns": [{"name": col[0], "description": col[1], "width": col[2]} for col in columns],
                    "select_where_columns": json.loads(select_where_columns),
                    "insert_columns": json.loads(insert_columns),
                    "update_columns": json.loads(update_columns),
                    "primary_key": json.loads(primary_key)
                }
                config_data["tables"].append(table_dict)
            return config_data
    except sqlite3.Error as error:
        print(f"讀取配置數據時發生錯誤：{error}")
        return None

# 從數據庫讀取配置並打印
config_from_db = load_config_from_db()
print(config_from_db)
