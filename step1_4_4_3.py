import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import step1_4_3_1 as util

"""
气温-冻融-年份聚类
"""

# 位置，因素，原始组合列名
pos = ['埃默里冰架',  '南极半岛', '毛德皇后地', '罗斯海']
fac = ['气温', '融化像元个数', ]
columns = [x + '（' + y + '）' for x in pos for y in fac]
filename = '/home/gjy/code/python3/myworks/resources/data'
num = 3


def read_csv(filename: str) -> list:
    """
    读取数据
    """
    df = pd.read_csv(filename + '.csv', header=0)
    lst1 = [df[['年'] + columns[i:i+2]].dropna() for i in range(0, 8, 2)]
    return lst1


def all_work():
    # font1 = '/home/gjy/.local/share/fonts/simfang.ttf' # 仿宋
    util.mpl_font('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
    ls = []
    ls1 = read_csv(filename)
    for name, df in zip(pos, ls1):
        grp = df.groupby('年')
        df = grp.mean()[grp.count() == 12].dropna()
        df.index, df['年'] = np.arange(df.shape[0]), df.index
        df['label'] = util.聚类((df - df.min()) / (df.max() - df.min()), num)
        # 聚类结果以最高温度递增的顺序排列
        # 各个类别的平均气温和平均融化面积
        mean, table = util.每类均值和映射表(df.iloc[:, [3, 0, 1]], num)
        # 绘图
        # util.draw([name, '年份', '气温', '融化面积'],
        #           df.iloc[:, [2, 0, 1, 3]],
        #           util.get_color(table, df['label']))
        # 分类结果
        t = [df.loc[df['label'] == i, '年'] for i in range(num)]
        t = ['"' + ','.join(map(str, t[table[i]])) + '"' for i in range(num)]
        t = pd.concat([mean, pd.DataFrame([t],
                      index=['年份'],
                      columns=np.arange(num))]).T
        t.columns = ['平均气温', '平均融化面积', '年份']
        t.name = name
        ls.append(t)
    # 输出为CSV文件
    t = pd.concat(ls)
    t.index = util.双层索引(pos, [0, 1, 2])
    print(t)
    t.to_csv('chore/年.csv')
    plt.show()


if __name__ == '__main__':
    all_work()
