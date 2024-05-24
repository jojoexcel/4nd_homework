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