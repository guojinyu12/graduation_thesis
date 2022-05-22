import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.cluster import KMeans

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


def draw(name: str, data: pd.DataFrame, color: np.ndarray):
    """
    显示图片
    """
    plt.figure()  # 新图
    ax1 = plt.axes(projection='3d')
    ax1.set_title(name, y=-0.1)  # plt.title(name)，下同
    ax1.set_xlabel('年份')
    ax1.set_ylabel(fac[0])
    ax1.set_zlabel('融化面积')  # plt 没有 z 轴
    # 创建这些样本的散点图
    ax1.scatter3D(data.iloc[:, 0], data.iloc[:, 1], data.iloc[:, 2],
                  c=color, s=10)
    plt.savefig(f'chore/{name}月.png', bbox_inches='tight')


def mpl_font(path: str):
    """
    字体设置
    """
    fontfamily = mpl.font_manager.FontProperties(fname=path).get_name()
    mpl.rcParams['font.family'] = fontfamily


def get_table(cls):
    """
    转换表
    """
    return [e.name for e in cls]


def get_color(table, label):
    """
    使得多个图形的相近分类颜色一致
    """
    table2 = [0] * len(table)
    for i, e in enumerate(table):
        table2[e] = i
    return np.fromiter((table2[e] for e in label), np.int32)


def 每月点数(df, table: list):
    grp = df.loc[:, ['月', 'label']].groupby('label')
    cls = [grp.get_group(i) for i in range(num)]
    cls = [e.groupby('月').count() for e in cls]
    t = [cls[table[i]] for i in range(num)]
    return pd.concat(t, axis=1)


def all_work():
    # font1 = '/home/gjy/.local/share/fonts/simfang.ttf' # 仿宋
    mpl_font('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
    ls = []
    ls1, ls2 = read_csv(filename)
    for name, df, df2 in zip(pos, ls1, ls2):
        # 聚类
        model = KMeans(n_clusters=num, random_state=135)
        df['label'] = model.fit_predict(df2)
        # 聚类结果以最高温度递增的顺序排列
        # 各个类别的平均气温和平均融化面积
        grp = df.iloc[:, 1:].groupby('label')
        cls = sorted((v for _, v in grp.mean().iterrows()),
                     key=lambda x: x.iat[0])
        t = pd.concat(cls, axis=1)
        t.columns = np.arange(num)
        ls.append(t)
        # 映射表
        table = get_table(cls)
        # 绘图
        draw(name, df, get_color(table, df['label']))
        # 分类结果
        ls.append(每月点数(df, table))
    # 输出为CSV文件
    t = pd.concat(ls[::2])
    t = t.reindex(index=columns[::2] + columns[1::2])
    a = ['平均气温', '平均融化面积']
    b = ['冬季', '过渡时期', '夏季']
    t.index = [[e1 for e1 in a for _ in pos],
               [e2 for e2 in pos] * len(a)]
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
