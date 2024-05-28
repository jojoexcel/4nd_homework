import math

def pad_to_width(s, width):
    """填充字符串以達到指定寬度，考慮到全角字符"""
    s = str(s)
    s_width = sum(2 if ord(char) > 127 else 1 for char in s)  # 計算字符串的顯示寬度
    padding = width - s_width  # 計算需要填充的空格數量

    if padding > 0:
        if padding % 2 == 0:
            return s + chr(12288) * (padding // 2)
        else:
            return s + chr(12288) * (padding // 2) + ' '
    return s  # 如果不需要填充，返回原字符串

def print_records(all_data, columns_name_tw, table_config, columns):
    if all_data:
        # 打印表頭
        header = "| " + " | ".join(pad_to_width(col, col_with["width"]) for col, col_with in zip(columns_name_tw, table_config["columns_set"])) + " |"
        print(header)

        # 打印分隔線
        # separator = "|-" + "-|-".join("-" * col_with["width2"] for col_with in table_config["columns_set"] if col_with["name"] in columns) + "-|"
        # print(separator)

        # 打印每一行數據
        for row in all_data:
            if len(row) == len(columns):
                formatted_row = "| " + " | ".join(pad_to_width(str(col), col_settings["width2"]) if col_settings["name"] in columns else pad_to_width(str(col), col_settings["width2"]) for col, col_settings in zip(row, table_config["columns_set"])) + " |"
                print(formatted_row)
            else:
                print("資料欄位數量與設定不符")
    else:
        print("無相符記錄")

# 示例用法
table_config = {
    "columns_set": [
        {"name": "title", "description": "書名", "width": 20, "width2": 20},
        {"name": "author", "description": "作者", "width": 20, "width2": 20},
        {"name": "publisher", "description": "出版社", "width": 20, "width2": 20},
        {"name": "year", "description": "年份", "width": 6, "width2": 6},
        {"name": "book_id", "description": "書籍ID", "width": 4, "width2": 4},
    ]
}

columns_name_tw = ["書名", "作者", "出版社", "年份"]
columns = ["title", "author", "publisher", "year"]
all_data = [
    ["簡愛", "夏綷蒂。姍蒂", "上海譯文出版社", 1847],
    ["紅樓夢", "曹雪芹", "人民文學出版社", 1792],
    ["西遊記", "吳承恩", "古典文學出版社", 1592],
    ["開心", "張開心", "碁石", 2045],
    ["python", "開", "基石", 2015]
]

print_records(all_data, columns_name_tw, table_config, columns)
