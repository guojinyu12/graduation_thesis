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
    wb: xl.Workbook = xl.load_workbook(filename)
    # 处理缺失数据
    ws = wb['1']

    for row in ws.iter_rows(max_col=13):
        # 处理缺失的融化像元数据，数据格式不一致，年份不一定有颜色
        if any(map(lambda x: x.font.color.rgb == 'FFFF0000', row)):
            row[2].value = row[3].value = row[4].value = row[5].value = ''
        # 处理缺失气温数据
        for x in row[9:]:
            if x.value == '-':
                x.value = ''
    wb.save(newfilename)


if __name__ == '__main__':
    filename = newfilename = None
    if len(sys.argv) == 1:
        filename = '/home/gjy/code/python3/myworks/resources/冻融范围和气温的时间序列.xlsx'
        newfilename = '/home/gjy/code/python3/myworks/resources/data.xlsx'
    elif len(sys.argv) == 3:
        filename = sys.argv[1]
        newfilename = sys.argv[2]
    else:
        print('用法: python3 step1.py [源文件 生成文件]')
        exit(1)
    step1(filename, newfilename)
