import pack.modu as lib
import os
import sqlite3

db_path = 'library.db'

# 檢查DB 是否存在
if not os.path.exists(db_path):
   #不存在
   DB_config_file = r'.\json\db_config.json'
   config = lib.config_load(DB_config_file)
   conn = lib.create_db(config)
   #匯入預設資料
   file = r'.\csv\users.csv'
   table_name = 'users'  # 指定要插入數據的表名
   lib.insert_users_from_file(file, table_name, config)
   file = r'.\json\books.json'
   table_name = 'books'  # 指定要插入數據的表名
   lib.insert_users_from_file(file, table_name, config)


attempts = 0
max_attempts = 3
while attempts < max_attempts:
    ck = lib.check_user()
    if ck == "密碼錯誤" or ck == "用戶不存在！":
        attempts += 1
        if attempts < max_attempts:
            print("重新輸入")
        else:
            print("錯誤次數過多，系統結束。")
            break
    else:
        print(ck)
        lib.display_menu()  # 显示菜单
        while True:
            choice = input("選擇要執行的功能(Enter離開)：")
            table_name = 'books'

            if choice == "1":
                lib.add_record()
            elif choice == "2":
                lib.delete_record()
            elif choice == "3":
                lib.modify_record()
            elif choice == "4":
                lib.select_books_like_title_or_author(db_path, table_name, config)
            elif choice == "5":


                lib.select_books_all()
            elif choice == "":
                print("程式結束")
                break
            else:
                print("=>無效的選擇")
