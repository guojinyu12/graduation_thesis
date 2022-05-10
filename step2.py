import numpy as np
import pandas as pd
import sklearn.cluster as skc
import matplotlib.pyplot as plt
import matplotlib as mpl


filename = 'resources/data.xlsx'
# 位置，因素，原始组合列名
pos = ['埃默里冰架',  '南极半岛', '毛德皇后地', '罗斯海']
fac = ['气温', '融化像元个数', ]
columns = [x + '（' + y + '）' for x in pos for y in fac]

# 读取数据，使用分层索引进行重排，改变列索引顺序。
df = pd.read_excel(filename, header=0, index_col=[0, 1],
                   usecols=['年', '月'] + columns)
df = df.reindex(columns=columns)
df.columns = [[p for p in pos for i in range(2)], fac * 4]
df2 = [df[name].dropna() for name in pos]
df_arr = [x.values for x in df2]


def draw(name: str, data, label: int, it):
    plt.title(name)
    # plt.xlabel(fac[1])
    # plt.ylabel(fac[0])
    for cluster in it:
        # 获取此群集的示例的行索引
        row_ix, = np.where(label == cluster)
        # 创建这些样本的散布
        plt.scatter(data.values[row_ix, 0], data.values[row_ix, 1])


# pos[0], 分界线 -52,-53
# 亲和力传播算法
# for linkage in ("ward", "average", "complete", "single"):
#     clustering = skc.AgglomerativeClustering(linkage=linkage, n_clusters=4)
#     label = clustering.fit_predict(df_arr[1])
#     draw(pos[1], df_arr[1], label, np.unique(label))


if __name__ == '__main__':
    # 字体设置
    path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
    prop = mpl.font_manager.FontProperties(fname=path)
    mpl.rcParams['font.family'] = prop.get_name()

    # plt.rcParams['axes.unicode_minus'] = False # 用来正常显示连字符
    for data, name, i in zip(df2, pos, [1, 2, 3, 4]):
        plt.figure(figsize=(6, 4))
        # plt.subplot(2, 2, i)
        # model = skc.AffinityPropagation(damping=0.9, preference=-50)
        # model = skc.KMeans(init='k-means++')
        model = skc.KMeans(n_clusters=3)
        # model = skc.MiniBatchKMeans(n_clusters=3)
        # model = skc.AgglomerativeClustering(n_clusters=3)
        # model = skc.Birch(threshold=0.01, n_clusters=3)
        # model = skc.DBSCAN(eps=5, min_samples=3)
        # bd = skc.estimate_bandwidth(data, quantile=0.2)
        # model = skc.MeanShift(bandwidth=bd, bin_seeding=True)
        label = model.fit_predict(data.values)
        draw(name, data, label, np.unique(label))
    plt.show()
