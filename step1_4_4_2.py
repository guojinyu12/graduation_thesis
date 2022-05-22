import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import step1_4_3_1 as util

"""
气温-冻融-月份聚类
"""

# 位置，因素，原始组合列名
pos = ['埃默里冰架',  '南极半岛', '毛德皇后地', '罗斯海']
fac = ['气温', '融化像元个数', ]
columns = [x + '（' + y + '）' for x in pos for y in fac]
filename = '/home/gjy/code/python3/myworks/resources/data'
num = 3


def read_csv(filename: str):
    """
    读取数据
    """
    df = pd.read_csv(filename + '.csv', header=0)
    lst1 = [df[['月'] + columns[i:i+2]].dropna() for i in range(0, 8, 2)]
    for i in df.index:
        if df.at[i, '月'] <= 3:
            df.at[i, '月'] += 12
    df = (df - df.min()) / (df.max() - df.min())
    lst2 = [df[['月'] + columns[i:i+2]].dropna() for i in range(0, 8, 2)]
    return lst1, lst2


def all_work():
    # font1 = '/home/gjy/.local/share/fonts/simfang.ttf' # 仿宋
    util.mpl_font('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
    ls = []
    ls1, ls2 = read_csv(filename)
    for name, df, df2 in zip(pos, ls1, ls2):
        # 聚类
        df['label'] = util.聚类(df2, num)
        # 聚类结果以最高温度递增的顺序排列
        # 各个类别的平均气温和平均融化面积
        t, table = util.每类均值和映射表(df.iloc[:, 1:], num)
        ls.append(t)
        # 绘图
        util.draw([name, '月份', '气温', '融化面积'],
                  df, util.get_color(table, df['label']))
        # 分类结果
        ls.append(util.每组点数('月', df[['月', 'label']], table, 3))
    # 输出为CSV文件
    t = pd.concat(ls[::2])
    t = t.reindex(index=columns[::2] + columns[1::2])
    a = ['平均气温', '平均融化面积']
    b = ['冬季', '过渡时期', '夏季']
    t.index = [[e for e in a for _ in pos],
               pos * len(a)]
    t.columns = b
    print(t)
    t.to_csv('chore/月.csv')
    t = pd.concat(ls[1::2], axis=1)
    t = t.reindex(index=np.arange(1, 13))
    t.columns = [[e for e in pos for _ in range(3)],
                 b * len(pos)]
    t = t.fillna(0)
    t.to_csv('chore/计数.csv')
    plt.show()


if __name__ == '__main__':
    all_work()
