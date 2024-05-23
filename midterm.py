import pack.moduv1 as lib
import os
import sqlite3


db_path = 'library.db'

# 檢查DB 是否存在
if os.path.exists(db_path):
    #存在
    conn = sqlite3.connect(db_path)

else:
   #不存在
   DB_config_file='db_config.json'
   config = lib.config_load(DB_config_file)
   conn = lib.create_db(config)
   conn.close()

   file='users.xls'
   lib.insert_users_from_file(file)
