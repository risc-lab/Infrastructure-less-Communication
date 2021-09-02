import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import random
from Graph import Graph

if __name__ == '__main__':
    # Input Handling

    n = input().split()
    node = [input().split() for i in range(int(n[1]))]

    g = Graph(int(n[0]))
    mapNode = {}
    R = 50

    for d in node:
        g.addEdge(int(d[0]), int(d[1]), int(d[2]))
        mapNode[int(d[0])] = [divmod(ele, R + 1) for ele in random.sample(range((R + 1) * (R + 1)), 1)][0]
        mapNode[int(d[1])] = [divmod(ele, R + 1) for ele in random.sample(range((R + 1) * (R + 1)), 1)][0]

    print(mapNode)

    mst = g.Update_DLT()
    connected = g.connectedComponents()
    print(mst)
    print(connected)

    # Visualizing Part

    if len(connected) == 1:

        colors = {}
        colorlist = ['r', 'g', 'b', 'c', 'm', 'y', 'brown', 'lime', 'orange', 'violet', 'pink', 'aqua', 'greenyellow']

        fig, axes = plt.subplots(figsize=(12, 8))
        plt.subplots_adjust(left=0.102)

        g = nx.Graph()

        for d in node:
            if int(d[0]) in connected[0] and int(d[1]) in connected[0]:
                g.add_edge(int(d[0]), int(d[1]), weight=int(d[2]))
                colors[int(d[0])] = 'silver'
                colors[int(d[1])] = 'silver'

        ps = []
        edgeList = [(u, v) for (u, v, d) in g.edges(data=True)]
        pos = {0: [0.3674637, 0.7622557], 1: [0.19043505, 0.14294067], 3: [0.6209852, 0.03839711], 5: [0.09155345, 0.38176054], 2: [0.8083849 , 0.98723054], 7: [0.7536171 , 0.47123492], 8: [0.18649153, 0.8147494 ], 4: [0.6978223, 0.1611038], 6: [0.04793257, 0.04406338], 9: [0.5678273 , 0.20682374], 10: [0.03874225, 0.5826505 ], 14: [0.7882373, 0.4411666], 12: [0.01260516, 0.9313917 ], 11: [0.11615593, 0.03466087], 13: [0.21466227, 0.11593232], 19: [0.6095732, 0.5971059], 16: [0.93620527, 0.80940473], 17: [0.30370563, 0.57918966], 18: [0.9473166 , 0.05444373], 15: [0.06531315, 0.38080773], 20: [0.529254  , 0.42149323]}
        ps.append(pos)
        values = [colors.get(node, 0.25) for node in g.nodes()]
        nx.draw_networkx_nodes(g, pos, node_size=250, node_color=values)

        nx.draw_networkx_edges(g, pos, edgeList, width=2)

        nx.draw_networkx_labels(g, pos, font_size=10, font_family='sans-serif')

        edge_labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=8, label_pos=0.4)

        DLT = []
        text = plt.text(0.5, -0.1, "", size=10, ha="center",
                        transform=axes.transAxes)

        l = []
        index = 0


        def update(num):
            # print(num)
            global l, index
            if num != 0:
                if (mst[num - 1][0], mst[num - 1][1]) in g.edges():
                    DLT.append(mapNode[mst[num - 1][0]])
                    DLT.append(mapNode[mst[num - 1][1]])
                    if colors[mst[num - 1][0]] != 'silver' and colors[mst[num - 1][1]] == 'silver':
                        colors[mst[num - 1][1]] = colors[mst[num - 1][0]]
                    elif colors[mst[num - 1][1]] != 'silver' and colors[mst[num - 1][0]] == 'silver':
                        colors[mst[num - 1][0]] = colors[mst[num - 1][1]]
                    elif colors[mst[num - 1][0]] == 'silver' and colors[mst[num - 1][1]] == 'silver':
                        colors[mst[num - 1][0]] = colorlist[index % len(colorlist)]
                        colors[mst[num - 1][1]] = colorlist[index % len(colorlist)]
                        index = index + 1
                    elif colors[mst[num - 1][0]] != 'silver' and colors[mst[num - 1][1]] != 'silver':
                        c0 = 0
                        c1 = 0
                        color0 = colors[mst[num - 1][0]]
                        color1 = colors[mst[num - 1][1]]
                        for key, val in colors.items():
                            if val == color0:
                                c0 = c0 + 1
                        for key, val in colors.items():
                            if val == color1:
                                c1 = c1 + 1
                        if c0 > c1:
                            for key, val in colors.items():
                                if val == color1:
                                    colors[key] = color0
                        else:
                            for key, val in colors.items():
                                if val == color0:
                                    colors[key] = color1
                    values = [colors.get(node, 0.25) for node in g.nodes()]
                    l = list(set(DLT))
                    nx.draw_networkx_edges(g, pos, edgelist=[(mst[num - 1][0], mst[num - 1][1])], width=5,
                                           edge_color='r')
                    nx.draw_networkx_nodes(g, pos, node_size=250, node_color=values)
                    # print(DLT)
            if num == len(mst):
                text.set_text(f"DLT: {l}")


        ani = animation.FuncAnimation(fig, update, frames=len(mst) + 1, interval=1000, repeat=False)
        # ani.save('../Visuals/animation.gif', writer='Pillow')
        manager = plt.get_current_fig_manager()
        plt.show()
