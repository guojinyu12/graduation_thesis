import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from statsmodels.tsa.stattools import grangercausalitytests


# 位置，因素，原始组合列名
pos = ['埃默里冰架',  '南极半岛', '毛德皇后地', '罗斯海']
fac = ['气温', '融化像元个数', ]
columns = [x + '（' + y + '）' for x in pos for y in fac]
filename = '/home/gjy/code/python3/myworks/resources/data'
"""
格兰杰因果检测
"""


def read_csv(filename: str):
    """
    读取数据
    """
    df = pd.read_csv(filename + '.csv', header=0, usecols=columns)
    lst1 = [df[columns[i:i+2]].dropna() for i in range(0, 8, 2)]
    return lst1


def mpl_font(path: str):
    """
    字体设置
    """
    fontfamily = mpl.font_manager.FontProperties(fname=path).get_name()
    mpl.rcParams['font.family'] = fontfamily


def gct(name: str, x, maxlag):
    print(name)

    gc = grangercausalitytests(x, maxlag, True, False)
    ssr_ftest = [val[0]['ssr_ftest'] for val in gc.values()]
    f_value, p_value, *_ = list(zip(*ssr_ftest))
    idx = np.argmax(f_value)
    t = ssr_ftest[idx]
    ft = round(t[0], 2)
    p = round(t[1], 4)
    print(f'{idx + 1} {ft:>5} p={p:.3}, F({int(t[2])},{int(t[3])})')

    # 绘图
    x = np.arange(1, maxlag + 1)
    fig, ax1 = plt.subplots()
    ax1.set_title(name)
    ax1.set_xlabel('范围')
    ax1.set_ylabel('统计量')
    line1, = ax1.plot(x, f_value)
    ax2 = ax1.twinx()  # 双坐标轴
    ax2.set_ylabel('p 值')
    line2, = ax2.plot(x, p_value, '--')
    plt.legend([line1, line2], ['统计量', 'p 值'], loc='best', frameon=False)
    plt.savefig(name + 'gct.png')


if __name__ == '__main__':
    # font1 = '/home/gjy/.local/share/fonts/simfang.ttf' # 仿宋
    mpl_font('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
    ls = read_csv(filename)
    for name, data in zip(pos, ls):
        gct(name + '1', data, 7)
    for name, data in zip(pos, ls):
        data = pd.concat([data.iloc[:, 1], data.iloc[:, 0]], axis=1)
        gct(name + '2', data, 7)
    plt.show()
