
import sys
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout,QHBoxLayout, QWidget,QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.font_manager as fm


class GraphViewer(QMainWindow): 
    def __init__(self):
        super().__init__()

        data = pd.read_csv('relation.csv',index_col=0)
        print(data)
        df = data.fillna(0) # NaN 값을 0으로 넣어주기
        listA = [] # 빈리스트 만들기
        for i in df.columns:
            for j in df.index:
                if df[i][j] != 0: # 호감도가 0이면 엣지 연결 안하기 위해서
                    tupleA = (i,j,df[i][j])
                    listA.append(tupleA)
        print(listA)

        g = nx.Graph()

        for node1, node2, score in listA:
            g.add_edge(node1, node2, weight = score) # node 모두 연결

        
        
        self.graph = g
        self.pos = nx.spring_layout(self.graph)  # 초기 노드 위치

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("NetworkX Graph Viewer")

        self.initUI()

    def initUI(self):
        self.target=''
        self.source=''

        # QWidget 클래스의 인스턴스를 생성
        self.central_wiget = QWidget() # 컨네이너 역할

        # QMainWindow의 중앙 위젯을 설정
        # QMainWindow의 중앙 영역에 self.central_widget에 할당한 QWidget 인스턴스가 배치된다.
        self.setCentralWidget(self.central_wiget) 

        self.canvas = FigureCanvas(plt.figure())  # 캔버스 생성

        # self.label1 = QLable("시작")
        # self.label2 = QLable(" 끝 ")

        

        # 입력 위젯 2개
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Enter a number")
        self.text_input2 = QLineEdit(self)
        self.text_input2.setPlaceholderText("Enter a number")

        # 라벨 2개
        label1 = QLabel('시작 : ',self)
        label2 = QLabel('끝 : ',self)
        
        self.label3 = QLabel(' ',self)
        self.label4 = QLabel(' ',self)

        # 입력 완료 버튼
        self.update_button = QPushButton("Update Graph" , self)
        self.update_button.clicked.connect(self.update_graph)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(label1)
        hbox1.addWidget(self.text_input)
        hbox1.addWidget(self.label3)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(label2)
        hbox2.addWidget(self.text_input2)
        hbox2.addWidget(self.label4)



        layout = QVBoxLayout()
       
        layout.addWidget(self.canvas)
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addWidget(self.update_button)

        self.central_wiget.setLayout(layout)

        # self.setCentralWidget(self.canvas)  # 캔버스를 중앙 위젯으로 설정
        
        self.canvas.mpl_connect('button_press_event', self.on_press)        # 이벤트 핸들러 (노드를 눌렀을 떄)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)      # 이벤트 핸들러 (노드를 움직일 떄)
        self.canvas.mpl_connect('button_release_event', self.on_release)    # 이벤트 핸들러 (노드를 놨을 때)
        self.update_button.clicked.connect(self.targetAndSorce)

        self.update_graph()  # 초기 그래프 업데이트

        self.dragging = False
        self.selected_node = None

    
    def update_graph(self):
        if self.target!='' and self.source!='':
            self.canvas.figure.clf()  # 기존 그래프 지우기
            ax = self.canvas.figure.add_subplot(111)

            # source = '주인'
            # target = '부하1'
            all_paths = nx.all_simple_edge_paths(self.graph,source=self.source, target= self.target)
            path_list = []
            for path in all_paths:
                for node in path:
                    for a in node:
                        path_list.append(a)

            path_list=list(set(path_list))
            print(path_list)

            edge_labels = {(u, v): d['weight'] for u, v, d in self.graph.edges(data=True)}

            color_list=[]
            for node in self.graph.nodes:
                if node == self.source or node == self.target:
                    color_list.append('yellow')
                elif node in path_list:
                    color_list.append('red')
                else:
                    color_list.append('blue')

            node_colors = ['red' if node in path_list else 'yellow' for node in self.graph.nodes]
            
            
            nx.draw(self.graph, self.pos, with_labels=True, node_size=1000, node_color=color_list, font_size=10, font_color='black', font_weight='bold', ax=ax, font_family='Malgun Gothic')
            

            nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=edge_labels, font_size=8, font_color='black')

            self.canvas.draw()

    def targetAndSorce(self):
        text1 = self.text_input.text()
        self.label3.setText(text1)
        self.source = text1

        text2 = self.text_input2.text()
        self.label4.setText(text2)
        self.target = text2

        self.update_graph()

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


if __name__ == '__main__':
    # G = grap() # csv 파일을 DataFrame으로 읽고 그래프로 만들기

    

    # QApplication은 PyQt에서 GUI 애플리케이션을 시작하는 데 사용되는 클래스이다.
    # 이 클래스의 인스턴스를 생성하면 QT 애플리케이션의 기본 환경을 설정한다.
    # QApplication 클래스의 인스턴스를 생성, sys.argv 변수는 Python 프로그램이 실행될 떄 전달된 명령줄 인수를 저장한다.
    app = QApplication(sys.argv)


    window = GraphViewer()
    window.show()
    sys.exit(app.exec_())






# 이벤트 핸들러는 이벤트가 발생했을 때 실행될 함수를 말한다.
# 이벤트 핸들러는 이벤트를 처리하기 위해 이벤트가 발생했을 때 실행될 함수를 등록하는 것으로 구현된다.
# 이벤트가 발생하면 등록된 이벤트 핸들러가 실행되며, 이를 통해 필요한 동작을 수행할 수 있다.

# while 문은 없지만 이벤트 핸들러를 통해 무한 루프를 실행한다. 즉, 사용자가 마우스 버튼을 놓을 때 까지 실행된다.

# 이벤트 핸들러는 canvas.mpl_connect() 함수로 만든다. 이 함수는 이벤트 유형과 이벤트 핸들럴 함수를 매개변수로 받는다.
# 이벤트 유형은 마우스 버튼 클릭, 마우스 움직임, 키보드 입력 등 다양한 이벤트를 나타낸다.
# 이벤트 핸들러 함수는 이벤트가 발생했을 때 호출되는 함수이다.

