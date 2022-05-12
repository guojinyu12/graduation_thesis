import numpy as np
import pandas as pd
import sklearn.cluster as skc
import matplotlib.pyplot as plt
import matplotlib as mpl
from statsmodels.tsa.stattools import grangercausalitytests


# 位置，因素，原始组合列名
pos = ['埃默里冰架',  '南极半岛', '毛德皇后地', '罗斯海']
fac = ['气温', '融化像元个数', ]
columns = [x + '（' + y + '）' for x in pos for y in fac]
filename = '/home/gjy/code/python3/myworks/resources/data'


def read_csv(filename: str) -> tuple:
    """
    读取数据
    """
    df = pd.read_csv(filename + '.csv', header=0,
                     usecols=['年', '月'] + columns)
    df2 = (df - df.min()) / (df.max() - df.min())
    lst1 = [df[['年', '月'] + columns[i:i+2]].dropna() for i in range(0, 8, 2)]
    lst2 = [df2[['年', '月'] + columns[i:i+2]].dropna() for i in range(0, 8, 2)]
    return lst1, lst2


def draw(name: str, data: pd.DataFrame, label: np.ndarray):
    """
    显示图片
    """
    ax1 = plt.axes(projection='3d')
    ax1.set_title(name)  # plt.title(name)，下同
    ax1.set_xlabel('年份')
    ax1.set_ylabel(fac[0])
    ax1.set_zlabel(fac[1])  # plt 没有 z 轴
    # 创建这些样本的散点图
    ax1.scatter3D(data.iloc[:, 0], data.iloc[:, 2], data.iloc[:, 3],
                  c=label)


def mpl_font(path: str):
    """
    字体设置
    """
    fontfamily = mpl.font_manager.FontProperties(fname=path).get_name()
    mpl.rcParams['font.family'] = fontfamily


def all_work():
    # font1 = '/home/gjy/.local/share/fonts/simfang.ttf' # 仿宋
    mpl_font('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
    df1, df2 = read_csv(filename)
    for i in range(len(pos)):
        model = skc.KMeans(n_clusters=3)
        data = df2[i]
        label: np.ndarray = model.fit_predict(data.iloc[:, [2, 3]])
        plt.figure()  # 新图
        # plt.subplot(2, 2, i)
        draw(pos[i], df1[i], label)
        grangercausalitytests(data.iloc[:, [2, 3]], 3, True)
    plt.show()


if __name__ == '__main__':
    all_work()
