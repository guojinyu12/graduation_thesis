import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

"""
气温数据特征
"""

# 位置，因素，原始组合列名
pos = ['埃默里冰架',  '南极半岛', '毛德皇后地', '罗斯海']
columns = [x + '（气温）' for x in pos]


def read_csv(filename: str) -> pd.DataFrame:
    """
    读取数据
    """
    df = pd.read_csv(filename + '.csv', header=0,
                     usecols=['年', '月'] + columns)
    return df


def mpl_font(path: str):
    """
    字体设置
    """
    fontfamily = mpl.font_manager.FontProperties(fname=path).get_name()
    mpl.rcParams['font.family'] = fontfamily
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def draw(name: str, x, y):
    plt.figure(figsize=(12, 4))
    plt.title(name)
    # 设置多少标签
    xlocator = mpl.ticker.LinearLocator(24)
    plt.gca().xaxis.set_major_locator(xlocator)
    plt.xticks(rotation=-30)    # 设置x轴标签旋转角度
    # 坐标轴名
    plt.xlabel('年月')
    plt.ylabel('气温/℃')
    plt.plot(x, y)


def ana(date, df):
    df2 = pd.DataFrame()
    for name, series in df.items():
        idx1 = np.argmin(series)
        idx2 = np.argmax(series)
        ls = [date[idx1], series.iloc[idx1], date[idx2], series.iloc[idx2]]
        df2 = pd.concat([df2, pd.DataFrame([ls], index=[name])])
    df2.columns = ['时期(min)', 'min', '时期(max)', 'max']
    return df2


if __name__ == '__main__':

    mpl_font('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
    df = read_csv('/home/gjy/code/python3/myworks/resources/data')
    年月 = df['年'].astype(str) + '-' + df['月'].astype(str)
    # 画图
    for e in columns:
        draw(e[:-4] + '月平均气温折线图', 年月, df[e])
        plt.savefig(e+'.png')
    # 统计
    print(df.iloc[:, 2:].describe())
    df.columns = ['年', '月'] + ['？' * (5 - len(e)) + e for e in pos]
    print(ana(年月, df.iloc[:, 2:]))
    grb = df.groupby('年')
    t = grb.max().iloc[:, 1:]
    print(t.describe())
    print(ana(t.index, t))
    t = grb.min().iloc[:-1, 1:]
    print(t.describe())
    print(ana(t.index, t))
