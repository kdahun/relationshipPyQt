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
  self.pos = nx.spring_layout(self.graph) # 초기 노드 위치

  self.setGeometry(100,100,800.600)
  self.setWindowTitle("NetworkX Graph Viewer")

  self.initUI()
```
