import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.cluster import KMeans


# 位置，因素，原始组合列名
pos = ['埃默里冰架',  '南极半岛', '毛德皇后地', '罗斯海']
fac = ['气温', '融化像元个数', ]
filename = '/home/gjy/code/python3/myworks/resources/data'
"""
k均值聚类
"""


def read_csv(filename: str):
    """
    读取数据
    """
    columns = [x + '（' + y + '）' for x in pos for y in fac]
    df = pd.read_csv(filename + '.csv', header=0, usecols=columns)
    t = [df[columns[i:i+2]] for i in range(0, len(columns), 2)]
    t = pd.concat(t, axis=1)
    return t.dropna()


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

    # 肘部法则
    elbow = []
    for i in range(1, 10):  # 创建遍历，找到最合适的k值
        kmeans = KMeans(n_clusters=i, init='k-means++', random_state=45)
        elbow.append(kmeans.fit(df).inertia_)
    # 通过画图找出最合适的K值
    t = [100]
    for i in range(1, len(elbow)):
        t.append((1 - elbow[i] / elbow[i - 1]) * 100)

    fig, ax1 = plt.subplots()
    ax1.set_xlabel('中心数/个')
    ax1.set_ylabel('SSE')
    line1, = ax1.plot(range(1, 10), elbow, 'bo-')
    ax2 = ax1.twinx()  # 双坐标轴
    ax2.set_ylabel('百分比')
    line2, = ax2.plot(range(1, 10), t, 'bv--')
    plt.legend([line1, line2], ['SSE', '百分比'], loc='best', frameon=False)
    plt.savefig('肘部法则.png')
    plt.show()
