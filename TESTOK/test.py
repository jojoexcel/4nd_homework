import os
import sqlite3
import pandas as pd
import json
import pack.modu as lib


def books_records(jsonfile):
    '''檢查 books 是否有資料'''
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    try:
        c.execute("SELECT title,author,publisher,year FROM books ")
        result_all = c.fetchall()
        # if not result_all:
        #     return read_books_file(jsonfile)
    except sqlite3.Error as error:
        print(f"查詢 books 作業發生錯誤：{error}")
        return 'error'
    conn.close()

def print_records(records):
    if records:
        print(f"|{'書名':{chr(12288)}^12}|{'作者':{chr(12288)}^12}|{'出版社':{chr(12288)}^12}|{'年份':^4}|")
        for row in records:
            print(f"|{row[0]:{chr(12288)}<12}|{row[1]:{chr(12288)}<12}|{row[2]:{chr(12288)}<12}|{row[3]:<6}|")
    else:
        print("無相符記錄")

def list_records():
    try:
        conn = sqlite3.connect("library.db")
        c = conn.cursor()
        c.execute("SELECT title,author,publisher,year FROM books ")
        result_all = c.fetchall()
        print_records(result_all)
        conn.close()
    except sqlite3.Error as error:
        print(f"查詢 books 作業發生錯誤：{error}")
