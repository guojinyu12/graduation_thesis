import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn import linear_model


# 位置，因素，原始组合列名
pos = ['埃默里冰架',  '南极半岛', '毛德皇后地', '罗斯海']
fac = ['气温', '融化像元个数', ]
filename = '/home/gjy/code/python3/myworks/resources/data'

"""
相关系数和最小二乘法
"""


def read_csv(filename: str):
    """
    读取数据
    """
    columns = [x + '（' + y + '）' for x in pos for y in fac]
    df = pd.read_csv(filename + '.csv', header=0,
                     usecols=['月'] + columns)
    df = pd.concat([df.iloc[:, 0], df.iloc[:, 1:5] * 625, df.iloc[:, 5:]],
                   axis=1)
    return df[(df['月'] <= 3) + (df['月'] >= 11)].iloc[:, 1:]


def draw(name: str, x, y):
    """
    显示图片
    """
    plt.figure(figsize=(12, 5))
    plt.title(name)
    plt.xlabel('气温/℃')
    plt.ylabel('融化面积/km²')  # plt 没有 z 轴
    # 创建这些样本的散点图
    plt.scatter(x, y, s=8)


def abline(slope, intercept):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    if intercept + slope * x_vals[0] < 0:
        y_vals[0] = 0
        x_vals[0] = -intercept / slope
    plt.plot(x_vals, y_vals, '--')


def text(txt):
    axes = plt.gca()
    x_vals = axes.get_xlim()
    x = x_vals[0] + (x_vals[1] - x_vals[0]) / 10
    y_vals = axes.get_ylim()
    plt.text(x, y_vals[1] * 9 / 10, txt)


def mpl_font(path: str):
    """
    字体设置
    """
    fontfamily = mpl.font_manager.FontProperties(fname=path).get_name()
    mpl.rcParams['font.family'] = fontfamily


def relation_work(name, df):
    x = df.iloc[:, 0]
    y = df.iloc[:, 1]
    # 散点图
    draw(name, x, y)

    # 线性回归折线
    x_ = x.values.reshape((len(x.index), 1))
    reg = linear_model.LinearRegression()
    reg.fit(x_, y)
    slope = round(reg.coef_[0], 2)
    intercept = round(y.mean() - x.mean() * reg.coef_[0], 2)
    abline(slope, intercept)

    # 相关系数
    r = round(df.corr().iloc[0, 1], 2)
    # 文本
    text(f"y = {slope}x + {intercept}\nr = {r}")
    plt.savefig(name + '.png')


if __name__ == '__main__':
    # font1 = '/home/gjy/.local/share/fonts/simfang.ttf' # 仿宋
    mpl_font('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
    columns = [x + '（' + y + '）' for x in pos for y in fac]
    df = read_csv(filename)
    df2 = None
    for i in range(len(pos)):
        c1 = columns[2 * i]
        c2 = columns[2 * i + 1]
        t = df[[c1, c2]].dropna()
        t.columns = [0, 1]
        if df2 is None:
            df2 = t
        else:
            df2 = pd.concat([df2, t])
        relation_work(pos[i], t)
    relation_work('南极', df2)
