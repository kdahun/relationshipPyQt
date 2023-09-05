# import sys
# import networkx as nx
# import matplotlib.pyplot as plt
# from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView
# from PyQt5.QtCore import Qt
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


# import pandas as pd
# import networkx as nx
# import matplotlib.pyplot as plt


# class GraphViewer(QMainWindow):
#     def __init__(self, graph):
#         super().__init__()

#         self.graph = graph
#         self.pos = nx.spring_layout(self.graph)  # 초기 노드 위치

#         self.setGeometry(100, 100, 800, 800)
#         self.setWindowTitle("NetworkX Graph Viewer")

#         self.initUI()

#     def initUI(self):
#         self.canvas = FigureCanvas(plt.figure())  # 캔버스 생성
#         self.setCentralWidget(self.canvas)  # 캔버스를 중앙 위젯으로 설정

#         self.canvas.mpl_connect('button_press_event', self.on_press)
#         self.canvas.mpl_connect('motion_notify_event', self.on_motion)
#         self.canvas.mpl_connect('button_release_event', self.on_release)

#         self.update_graph()  # 초기 그래프 업데이트

#         self.dragging = False
#         self.selected_node = None

#     def update_graph(self):
#         self.canvas.figure.clf()  # 기존 그래프 지우기
#         ax = self.canvas.figure.add_subplot(111)

#         nx.draw(self.graph, self.pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=10, font_color='black', font_weight='bold', ax=ax)

#         self.canvas.draw()

#     def on_press(self, event):
#         if event.button == 1:
#             x, y = event.xdata, event.ydata
#             for node, (nx, ny) in self.pos.items():
#                 if abs(x - nx) <= 0.05 and abs(y - ny) <= 0.05:  # 노드 위치 근처를 클릭했을 때
#                     self.selected_node = node
#                     self.dragging = True
#                     self.offset = (x - nx, y - ny)
#                     break

#     def on_motion(self, event):
#         if self.dragging:
#             x, y = event.xdata, event.ydata
#             self.pos[self.selected_node] = (x - self.offset[0], y - self.offset[1])
#             self.update_graph()

#     def on_release(self, event):
#         self.dragging = False
#         self.selected_node = None



# if __name__ == '__main__':

    


#     G = grap()
#     #

#     app = QApplication(sys.argv)
#     window = GraphViewer(G)
#     window.show()
#     sys.exit(app.exec_())

import sys
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class GraphViewer(QMainWindow): 
    def __init__(self, graph):
        super().__init__()

        self.graph = graph
        self.pos = nx.spring_layout(self.graph)  # 초기 노드 위치

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("NetworkX Graph Viewer")

        self.initUI()

    def initUI(self):
        self.canvas = FigureCanvas(plt.figure())  # 캔버스 생성
        self.setCentralWidget(self.canvas)  # 캔버스를 중앙 위젯으로 설정

        self.canvas.mpl_connect('button_press_event', self.on_press)        # 이벤트 핸들러 (노드를 눌렀을 떄)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)      # 이벤트 핸들러 (노드를 움직일 떄)
        self.canvas.mpl_connect('button_release_event', self.on_release)    # 이벤트 핸들러 (노드를 놨을 때)

        self.update_graph()  # 초기 그래프 업데이트

        self.dragging = False
        self.selected_node = None

    def update_graph(self):
        self.canvas.figure.clf()  # 기존 그래프 지우기
        ax = self.canvas.figure.add_subplot(111)

        nx.draw(self.graph, self.pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=10, font_color='black', font_weight='bold', ax=ax)

        self.canvas.draw()

    def on_press(self, event):
        if event.button == 1:
            x, y = event.xdata, event.ydata
            for node, (nx, ny) in self.pos.items():
                if abs(x - nx) <= 0.1 and abs(y - ny) <= 0.1:  # 노드 위치 근처를 클릭했을 때
                    self.selected_node = node
                    self.dragging = True
                    self.offset = (x - nx, y - ny)
                    break

    def on_motion(self, event):
        if self.dragging:
            x, y = event.xdata, event.ydata
            self.pos[self.selected_node] = (x - self.offset[0], y - self.offset[1])
            self.update_graph()

    def on_release(self, event):
        if event.button == 1:
            self.dragging = False
            self.selected_node = None
            print(self.pos)

def grap():
    data=pd.read_csv('relation.csv',index_col=0)
    print(data)
    df = data.fillna(0) # NaN 값을 0으로 넣어주기

    listA = [] # 호감도가 1이상인 값을 갖는 튜플을 가지고 있는 리스트


    for i in df.columns:
        for j in df.index:
            if df[i][j]!=0: # 호감도가 0이 아니면 튜플에 넣어 준다.
                tupleA = (i,j,df[i][j])
                listA.append(tupleA)
    print(listA)

    # 데이터를 기반으로 그래프에 노드와 엣지 추가
    edge_weights = {}

    g = nx.Graph()

    for node1, node2, score in listA:
        g.add_edge(node1, node2, weight=score)

    # a에서 b로 이동할 수 있는 모든 경로 찾기
    all_paths = nx.all_simple_paths(g, source='주인', target='부하1')

    # 모든 노드를 파란색으로 표시하기 위해 노드 색상 설정
    node_colors = ['blue'] * len(g.nodes)

    # 경로 상의 노드를 빨간색으로 표시하기 위해 노드 색상 설정
    for path in all_paths:
        for node in path:
            node_colors[list(g.nodes).index(node)] = 'red'

    # 그래프 시각화
    plt.figure(figsize=(20, 20))
    edge_widths = [1.5 * g[u][v]['weight'] for u, v in g.edges()]
    pos = nx.spring_layout(g, seed=1)
    pos['a'] = (0, 5)

    nx.draw_networkx(g, pos, with_labels=True, width=edge_widths, node_size=8000, node_color=node_colors)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_weights, font_size=30)
    plt.axis('off')
    return g

if __name__ == '__main__':
    G = grap() # csv 파일을 DataFrame으로 읽고 그래프로 만들기


    # QApplication은 PyQt에서 GUI 애플리케이션을 시작하는 데 사용되는 클래스이다.
    # 이 클래스의 인스턴스를 생성하면 QT 애플리케이션의 기본 환경을 설정한다.
    # QApplication 클래스의 인스턴스를 생성, sys.argv 변수는 Python 프로그램이 실행될 떄 전달된 명령줄 인수를 저장한다.
    app = QApplication(sys.argv)


    window = GraphViewer(G)
    window.show()
    sys.exit(app.exec_())






# 이벤트 핸들러는 이벤트가 발생했을 때 실행될 함수를 말한다.
# 이벤트 핸들러는 이벤트를 처리하기 위해 이벤트가 발생했을 때 실행될 함수를 등록하는 것으로 구현된다.
# 이벤트가 발생하면 등록된 이벤트 핸들러가 실행되며, 이를 통해 필요한 동작을 수행할 수 있다.

# while 문은 없지만 이벤트 핸들러를 통해 무한 루프를 실행한다. 즉, 사용자가 마우스 버튼을 놓을 때 까지 실행된다.

# 이벤트 핸들러는 canvas.mpl_connect() 함수로 만든다. 이 함수는 이벤트 유형과 이벤트 핸들럴 함수를 매개변수로 받는다.
# 이벤트 유형은 마우스 버튼 클릭, 마우스 움직임, 키보드 입력 등 다양한 이벤트를 나타낸다.
# 이벤트 핸들러 함수는 이벤트가 발생했을 때 호출되는 함수이다.

