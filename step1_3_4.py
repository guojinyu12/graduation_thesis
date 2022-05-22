import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl


# 位置，因素，原始组合列名
pos = ['埃默里冰架',  '南极半岛', '毛德皇后地', '罗斯海']
fac = ['气温', '融化像元个数', ]
filename = '/home/gjy/code/python3/myworks/resources/data'

"""
季节性分析
"""


def read_csv(filename: str):
    """
    读取数据
    """
    columns = [x + '（' + y + '）' for x in pos for y in fac]
    df = pd.read_csv(filename + '.csv', header=0,
                     usecols=['月'] + columns)
    return df


def draw(name: list, x, ys):
    """
    显示图片
    """
    plt.figure()
    plt.xlabel(name[0])
    plt.ylabel(name[1])  # plt 没有 z 轴
    mark = ['-', '--', '-.', ':']
    # 创建这些样本的散点图
    t = [plt.plot(x, y[1], m)[0] for y, m in zip(ys.iteritems(), mark)]
    plt.legend(t, pos, loc='best', frameon=False)
    plt.savefig('chore/' + name[0] + name[1][:2] + '.png',
                bbox_inches='tight')


def mpl_font(path: str):
    """
    字体设置
    """
    fontfamily = mpl.font_manager.FontProperties(fname=path).get_name()
    mpl.rcParams['font.family'] = fontfamily


if __name__ == '__main__':
    # font1 = '/home/gjy/.local/share/fonts/simfang.ttf' # 仿宋
    mpl_font('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
    df = read_csv(filename)
    df = df.groupby('月').mean()
    draw(['月份', '融化面积/km²'], df.index, df.iloc[:, :4])
    draw(['月份', '气温/℃'], df.index, df.iloc[:, 4:])
    plt.show()
