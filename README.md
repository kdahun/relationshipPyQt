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
