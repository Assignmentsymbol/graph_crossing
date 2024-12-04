import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# 创建一个图
G = nx.erdos_renyi_graph(30, 0.2)

# 固定图的显示大小
plt.figure(figsize=(8, 6))

# 创建初始布局
pos = nx.spring_layout(G)

# 绘制初始图形
nx.draw_networkx(G, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10, width=2)

# 设置固定的坐标轴范围和比例
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.axis('equal')

while True:
    userIn = input("redo?[y/n]:  ")
    while userIn == 'y':
        # 动态更新：例如，改变节点颜色并刷新图形
        for i in range(10):
            # 每次改变节点颜色
            node_colors = np.random.rand(len(G.nodes))  # 随机改变节点颜色

            # 清除当前图形
            plt.clf()

            # 重新绘制图形，更新节点颜色
            nx.draw_networkx(G, pos, with_labels=True, node_size=500, node_color=node_colors, font_size=10, width=2)

            # 设置坐标轴范围和比例
            plt.xlim(-1, 1)
            plt.ylim(-1, 1)
            plt.axis('equal')

            # 更新图形
            plt.draw()  # 更新当前图形内容，但不弹出新窗口

            # 暂停一段时间（比如100毫秒），模拟动态变化
            plt.pause(0.1)
            userIn = ''

# plt.show()
