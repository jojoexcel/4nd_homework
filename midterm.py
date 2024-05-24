import pack.modu as lib
import os
import sqlite3


db_path ='library.db'

# 檢查DB 是否存在
if os.path.exists(db_path):
    #存在
    conn = sqlite3.connect(db_path)


else:
   #不存在
   DB_config_file=r'.\json\db_config.json'
   config = lib.config_load(DB_config_file)
   conn = lib.create_db(config)
   file =r'.\csv\users.csv'
   table_name = 'users'  # 指定要插入數據的表名
   lib.insert_users_from_file(file, table_name, config)
   file=r'.\json\books.json'
   table_name = 'books'  # 指定要插入數據的表名
   lib.insert_users_from_file(file, table_name, config)

