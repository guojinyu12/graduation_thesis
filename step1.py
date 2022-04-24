import openpyxl as xl
import os
import sys


def step1(filename: str, newfilename: str) -> None:
    if not os.path.exists(filename):
        print(f'{filename} 不存在。')
        exit(1)
    if os.path.exists(newfilename):
        print(f'{newfilename} 已存在。')
        exit(1)
    wb = xl.load_workbook(filename)
    del wb['Sheet1']  # 删除'Sheet1'表
    # 处理缺失数据
    ws = wb['1']
    # ws.delete_cols(7) # 删除空行
    for row in ws.rows:
        # 数据格式不一致，年份不一定有颜色
        if any(map(lambda x: x.font.color.rgb == 'FFFF0000', row)):
            row[2].value = row[3].value = row[4].value = row[5].value = ''
    wb.save(newfilename)


if __name__ == '__main__':
    filename = newfilename = None
    if len(sys.argv) == 1:
        filename = './resources/冻融范围和气温的时间序列.xlsx'
        newfilename = './resources/data.xlsx'
    elif len(sys.argv) == 3:
        filename = sys.argv[1]
        newfilename = sys.argv[2]
    else:
        print('用法: python3 step1.py [源文件 生成文件]')
        exit(1)
    step1(filename, newfilename)
