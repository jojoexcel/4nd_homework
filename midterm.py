import pack.modu as lib
import sqlite3
import json
import csv


# 檢查資料庫是否存在，若不存在則建立並初始化
ckack_db=lib.create_database()
if ckack_db:
    lib.datain()



# 使用者登入
logged_in = False
while not logged_in:
    username = input("請輸入帳號：")
    password = input("請輸入密碼：")
    user = lib.login(username, password)
    if user:
        logged_in = True
    # else:
        # print("帳號或密碼錯誤，請重新輸入")

# # 顯示選單並執行相應操作
logged_in = True
count_chang=0
while True:
    try:
        choice = lib.show_menu()
        if choice == '1':
            count_valu=False
            count_valu=lib.add_record()
            if count_valu :
                count_chang+=1
                print (f"異動 {count_chang} 記錄")

        elif choice == '2':
            count_valu=False
            lib.list_records()
            count_valu=lib.delete_record()
            if count_valu :
                count_chang+=1
                print (f"異動 {count_chang} 記錄")
        elif choice == '3':
            count_valu=False
            lib.list_records()
            count_valu=lib.update_record()
            if count_valu :
                count_chang+=1
                print (f"異動 {count_chang} 記錄")
        elif choice == '4':
            lib.search_record()
        elif choice == '5':
            lib.list_records()
        elif choice == '':
            break

        else:
            print("無效的選擇")


    except csv.Error as e:
        print(f"{e}")
    except json.JSONDecodeError as e:
        print(f"{e}")
    except sqlite3.Error as e:
        print(f"{e}")
    except ValueError as e:
        print(f"{e}")
    except Exception as e:
        print(f"{e}")


