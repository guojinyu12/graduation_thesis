import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

"""
冻融数据
"""
# 位置，因素，原始组合列名
pos = ['埃默里冰架',  '南极半岛', '毛德皇后地', '罗斯海']
columns = [x + '（融化像元个数）' for x in pos]


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
    plt.title(name + '融化面积折线图')
    # 设置多少标签
    xlocator = mpl.ticker.LinearLocator(24)
    plt.gca().xaxis.set_major_locator(xlocator)
    plt.xticks(rotation=-30)    # 设置x轴标签旋转角度
    # 坐标轴名
    plt.xlabel('年月')
    plt.ylabel('融化面积/km²')
    plt.plot(x, y)


def ana(date, df):
    df2 = pd.DataFrame()
    for name, series in df.items():
        idx1 = np.argmin(series)
        idx2 = np.argmax(series)
        ls = [date[idx2], series.iloc[idx2], date[idx1], series.iloc[idx1]]
        df2 = pd.concat([df2, pd.DataFrame([ls], index=[name])])
    df2.columns = ['时期(max)', 'max', '时期(min)', 'min']
    return df2


def get_new_years(it):
    c = itertools.count(0)
    ls = [-1]
    for e in it:
        if e == 4:
            ls.append(next(c))
        else:
            ls.append(ls[-1])
    return ls[1:]


if __name__ == '__main__':

    mpl_font('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
    df = read_csv('/home/gjy/code/python3/myworks/resources/data')
    df = pd.concat([df.iloc[:, :2], df.iloc[:, 2:] * 625], axis=1)
    年月 = df['年'].astype(str) + '-' + df['月'].astype(str)
    # 画图
    for e in columns:
        draw(e[:-8], 年月, df[e])
        plt.savefig(e + '.png', bbox_inches='tight')
    # plt.show()
    df.columns = ['年', '月'] + ['？' * (5 - len(e)) + e for e in pos]
    df2 = df.iloc[:, 2:]
    # 统计
    print(ana(年月, df2))
    print()
    print("夏季平均值：")
    df3 = df2[(df['月'] <= 3) + (df['月'] >= 11)]
    print(df3.mean())
    print()

    df2['融化周期'] = get_new_years(df['月'])
    print('最高月：')
    grb = df2.groupby('融化周期')
    t = grb.max()
    print(t.describe())
    print(ana(t.index + 1979, t))
    print()
