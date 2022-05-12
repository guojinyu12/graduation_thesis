import pandas as pd

# 位置，因素，原始组合列名
pos = ['埃默里冰架',  '南极半岛', '毛德皇后地', '罗斯海']
fac = ['气温', '融化像元个数', ]
columns = [x + '（' + y + '）' for x in pos for y in fac]


"""
读取数据
"""
dirname = '/home/gjy/code/python3/myworks/resources/'
filename = dirname + 'data.xlsx'
df = pd.read_excel(filename, header=0, index_col=[0, 1],
                   usecols=['年', '月'] + columns)
df.to_csv(dirname + 'data.csv')
