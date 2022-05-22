import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.cluster import KMeans


def draw(name: list, data: pd.DataFrame, color: np.ndarray):
    """
    显示图片
    """
    plt.figure()  # 新图
    ax1 = plt.axes(projection='3d')
    ax1.set_title(name[0], y=-0.1)  # plt.title(name)，下同
    ax1.set_xlabel(name[1])
    ax1.set_ylabel(name[2])
    ax1.set_zlabel(name[3])  # plt 没有 z 轴
    # 创建这些样本的散点图
    ax1.scatter3D(data.iloc[:, 0], data.iloc[:, 1], data.iloc[:, 2],
                  c=color, s=10)
    plt.savefig(f'chore/{name[0] + name[1]}.png', bbox_inches='tight')


def mpl_font(path: str):
    """
    字体设置
    """
    fontfamily = mpl.font_manager.FontProperties(fname=path).get_name()
    mpl.rcParams['font.family'] = fontfamily


def get_color(table, label):
    """
    使得多个图形的相近分类颜色一致
    """
    table2 = [0] * len(table)
    for i, e in enumerate(table):
        table2[e] = i
    return np.fromiter((table2[e] for e in label), np.int32)


def 每类均值和映射表(df, num: int):
    grp = df.groupby('label')
    cls = sorted((v for _, v in grp.mean().iterrows()),
                 key=lambda x: x.iat[0])
    t = pd.concat(cls, axis=1)
    t.columns = np.arange(num)
    table = [e.name for e in cls]
    return t, table


def 每组点数(name, df, table: list, num: int):
    grp = df.groupby('label')
    cls = [grp.get_group(i) for i in range(num)]
    cls = [e.groupby(name).count() for e in cls]
    t = [cls[table[i]] for i in range(num)]
    return pd.concat(t, axis=1)


def 聚类(df, num: int):
    model = KMeans(n_clusters=num, random_state=135)
    return model.fit_predict(df)


def 双层索引(a: list, b: list) -> list:
    return [[e for e in a for _ in b], b * len(a)]
