def calculate_rectangle_area(length, width):
    assert isinstance(length, (int, float)), "長度必須是數值型別"
    assert isinstance(width, (int, float)), "寬度必須是數值型別"
    assert length > 0, "長度必須為正數"
    assert width > 0, "寬度必須為正數"
    return length * width

print(calculate_rectangle_area(-1, 5))        # 引發 AssertionError: 長度必須為正數

print(calculate_rectangle_area(2, 'hello'))   # 引發 AssertionError: 寬度必須是數值型別

print(calculate_rectangle_area(3, 4))