# relationshipPyQt

```
import sys
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
```

* 'sys' : 시스템 관련 기능을 사용하기 위한 모듈
* 'pandas' : 데이터 분석 및 조작을 위한 라이브러리
* 'networkx' : 그래프 분석을 위한 라이브러리
* 'matplotlib.pyplot' : 그래프 시각화를 위한 라이브러리
* 'PyQt5.QtWidgets' : PyQt5 라이브러리에서 GUI 위젯을 사용하기 위한 모듈
* 'matplotlib.backends.backend_qt5agg.FigureCanbasQTAgg' : Matplotlib 그래프를 PyQt5 위젯에 표시하기 위한 모듈이다.

---
## GraphViewer 클래스를 정의한다.
```
class GraphViewer(QMainWindow):
```
* 'GraphViewer' 클래스는 PyQt5의 QMainWindow 클래스를 상속하여 그래프를 표시할 윈도우를 만드는 역할을 한다.

---
##  __init__ 메서드에서 클래스 초기화를 수행한다.
```
def __init__(self, graph):
  super().__init__()

  self.graph = graph
  self.pos = nx.spring_layout(self.graph)           # 초기 노드 위치

  self.setGeometry(100,100,800.600)                 # 윈도우 크기 설정
  self.setWindowTitle("NetworkX Graph Viewer")      # title 변경

  self.initUI()
```
* '__init__' 메서드는 클래스의 생성자로, 객체가 생성될 떄 호출된다. 그래프('graph')를 받아 초기화하고, 윈도우의 위치, 크기, 제목 등을 설정한다. 그리고 'initUI' 메서드를 호출하여 사용자 인터페이스를 초기화 한다.

---
## initUI 메서드에서 사용자 인터페이스를 초기화한다.
```
def initUI(self):
  self.canvas = FigureCanvas(plt.figure())                          # 캔버스 생성
  self.setCentralWidget(self.canvas)                                # 캔버스를 중앙 위젯으로 설정

  self.canvas.mpl_connect('button_press_event', self.on_press)      # 노드를 클릭했을 떄 핸들링 이벤트
  self.canvas.mpl_connect('motion_notify_evnet', self.on_motion)    # 노드를 잡고 드래그 중일 떄 핸들링 이벤트
  self.canvas.mpl_connect('button_release_event', self.on_release)  # 노드를 놨을 때 핸들링 이벤트

  self.update_graph()                                               # 초기 그래프 업데이트

  self.dragging = False
  self.selected_node = None
```

* self.canvas = FigureCanvas(plt.figure()) : Matplotlib를 사용하여 그래프를 그리기 위한 캔버스를 생성한다.
  plt.figure() 함수는 새로운 Matplotlib Figure 객체를 생섣하고, 이를 FigureCanvas에 넣어서 캔버스를 생섣한다.
  
* self.setCentralWidget(self.canvas) : 캔버스를 QMainWindow의 중앙 위젯으로 설정한다.

* self.canvas.mpl_connect(...) : 캔버스에 이벤트 핸들러를 연결한다.
  1. button_press_event , self.on_press : 마우스 버튼을 눌렀을 때 호출되는 이벤트 핸들러로, 노드를 눌렀을 때 실행된다.
  2. motion_notify_event, self.on_motion : 마우스를 이돌할 떄 호출되는 이벤트 핸들러로, 노드를 움직일 떄 실행된다.
  3. button_release_event, self.on_release : 마우스 버튼을 놓았을 때 호출되는 이벤트 핸들러로, 노드를 놨을 때 실행된다.
 
* self.update_graph() : 초기 그래프를 업데이트 한다. 이 함수는 그래프를 그리는 역할을 한다.

* self.dragging = False와 self.selected_node = None : 드래그 상태와 선택된 노드를 나타내는 변수를 초기화한다.
  드래그가 아직 시작되지 않았으므로 self.dragging은 False로 설정하고, 선택된 노드가 없으므로 self.dragging은 False로 설정하고 선택된 노드가 없으므로 self.selected_node은 None으로 설정된다.

이렇게 초기화된 사용자 인터페이스는 그래프를 표시하고, 마우스 이벤트를 처리하며 노드를 이동할 수 있는 기능을 제공한다

---
## update_graph 메서드에서 그래프 업데이트
```
def update_graph(self):
  self.canvas.figure.clf()  #  기존 그래프 지우기
  ax = self.canvas.figure.add_subplot(111)

  nx.draw(self.graph, self.pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=10, font_color='black', font_weight='bold', ax=ax)

  self.canvas.draw()
```
* self canvas.figure.clf() : 기존 그래프를 지우기 위해 Matplotlib Figure 객체를 클리어 한다. 이렇게 하면 이전에 그려진 그래프를 모두 삭제한다.

* ax = self.canvas.figure.add_subplot(111) : 그래프를 그릴 서브플롯(서브그림)을 생성한다. 111은 하나의 그림과 하나의 그림을 가진 그림 영역을 의미한다.
  1) Matplotlib에서 그림(figure)은 하나의 그래프나 도표를 나타낸다. 그림 내에는 여려 개의 서브 플롯을 생성하여 여려 개의 그래프를 동시에 표시할 수 있다. 각 서브플롯은 그림 내의 작은 영역을 의미한다.
  2) self.canvas.figure 는 현재 그림을 나타내는 Matplotlib Figure 객체이다.
  3) add_subplot(111) 은 서브플롯을 그림에 추가하는 메서드이다.괄호 안의 인수는 서브플롯의 위치 및 배치를 지정한다.
     * 첫 번째 숫자 : 격자의 행 수
     * 두 번째 숫자 : 격자의 열 수
     * 세 번째 숫자 : 그림 번호
     * 111은 그림을 하나의 행과 열로 나누고 하나의 그림을 그린다는 것을 의미한다.
  4) nx.draw(...) : Networkx 의 nx.draw 함수를 사용하여 그래프를 그린다.
     * self.graph : 그래프 객체
     * self.pos : 노드의 위치 정보를 담고 있는 딕셔너리
     * with_labels = True : 노드에 라벨을 표시
     * node_size = 1000 : 노드의 크기를 설정
     * node_color = 'skyblue' : 노드의 색상을 설정
     * font_size = 10 : 라벨의 폰트 크기를 설정
     * font_color = 'black' : 라벨의 폰트 색상을 설정
     * font_weight = 'bold' : 라벨의 글꼴 두께를 설정
     * ax = ax : 앞에서 생성한 서브플롯을 사용하여 그래프
  5) self.canvas.draw() : 그래프를 그린후, Maplotlib 캔버스를 다시 그림
