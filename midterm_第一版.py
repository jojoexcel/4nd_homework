import pack.modu_第一版 as lib
import os

db_path = 'library.db'
DB_config_file = r'.\json\db_config.json'
config = lib.config_load(DB_config_file)

# 檢查DB 是否存在
if not os.path.exists(db_path):
    # 不存在
    conn = lib.create_db(config)
    # 匯入預設資料
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
        if not attempts < max_attempts:
            print("錯誤次數過多，系統結束。")
            break
    else:
        print(ck)

        while True:
            # lib.clear_screen()  # 清理屏幕（如果需要）
            lib.display_menu()  # 顯示菜單
            choice = input("選擇要執行的功能(Enter離開)：")

            if choice == "1":
                table_name = "books"
                fun_json = "insert_columns"
                ckrun = lib.data_insert(table_name, config, fun_json)
                if 'ckrun' in locals() and ckrun:
                    print(f"異動 {ckrun} 記錄")
                lib.select_books_all()
            elif choice == "2":
                lib.select_books_all()
                table_name = "books"
                fun_json = "primary_key"
                ckrun = lib.data_delete(table_name, config, fun_json)
                if 'ckrun' in locals() and ckrun:
                    print(f"異動 {ckrun} 記錄")
                lib.select_books_all()
            elif choice == "3":
                lib.select_books_all()
                table_name = "books"
                fun_json = "update_columns"
                ckrun = lib.data_update(table_name, config, fun_json)
                if 'ckrun' in locals() and ckrun:
                    print(f"異動 {ckrun} 記錄")
                lib.select_books_all()
            elif choice == "4":
                table_name = "books"
                fun_json = "select_columns"
                lib.select_books_like_title_or_author(table_name, config, fun_json)
            elif choice == "5":
                lib.select_books_all()
            elif choice == "":
                print("程式結束")
                break
            else:
                print("=>無效的選擇")
        break
