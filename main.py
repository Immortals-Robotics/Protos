import sys


from Vision.vision import *
from draw import *
from Debug.debug import *

class Logger(QWidget):
    def __init__(self):
        super().__init__()

        self.vision = Vision()
        self.vision.start()

        self._vision_control = {
            'connect': QPushButton("Vision Connect"),
            'disconnect': QPushButton("Vision Disconnect")
        }


        self.initUI()

        
    def initUI(self):
        self.setGeometry(200, 200, 800, 500)
        self.setWindowTitle('Logger')
        main_layout = QGridLayout()
        main_layout.addLayout(self._ui_control(), 0, 0)
        main_layout.addLayout(self._ui_vision(), 0, 1, 1, 6)
        self.setLayout(main_layout)        
        self.show()
    
    def _ui_control(self):
        layout = QGridLayout()

        layout.addWidget(self._vision_control['connect'], 0, 0, 1, 1)
        layout.addWidget(self._vision_control['disconnect'], 1, 0, 1, 1)
        for i in range(5):
            layout.addWidget(QPushButton("Button " + str(i)))

        self._config_onClick_listener()
        return layout

    def _config_onClick_listener(self):
        self._vision_control['connect'].clicked.connect(self.onClick_vision_connect)
        self._vision_control['disconnect'].clicked.connect(self.onClick_vision_disconnect)

    def _ui_vision(self):
        layout = QHBoxLayout()
        self.board_view = Board(self)
        self.draw = Draw(self.board_view)

        self.vision.graphic_ready.connect(self.draw.add2queue)

        layout.addWidget(self.board_view)
        return layout

    def onClick_vision_connect(self):
        if not self.vision.isConnected():
            self.vision.connect()

    def onClick_vision_disconnect(self):
        if self.vision.isConnected():
            self.vision.disconnect()

class Board(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        self.height = 450
        self.width = 4 * self.height / 3.0
        self.setFixedWidth(self.width + 30)
        self.setFixedHeight(self.height + 30)

        self.setScene(QGraphicsScene(0, 0, self.width, self.height, self))
        self.setStyleSheet("background-color:rgb(77,186,21);")
        self.setSceneRect(QRectF(self.viewport().rect()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Logger()
    sys.exit(app.exec_())