from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QGridLayout
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor
from PyQt5.QtCore import Qt
from PyQt5 import uic
from random import randint
from untitled import Ui_MainWindow


class Test(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.setFixedSize(100, 100)
        self.ui.pushButton.clicked.connect(self.draw)

        self.ui.label = QLabel()
        canvas = QPixmap(600, 600)
        self.ui.label.setPixmap(canvas)

        self.ui.layout = QGridLayout(self.ui.centralwidget)
        self.ui.layout.addWidget(self.ui.pushButton, 0, 0, alignment=Qt.AlignCenter)
        self.ui.layout.addWidget(self.ui.label, 1, 0)

    def draw(self):
        v = randint(10, 100)
        x, y = [randint(10, 500) for i in range(2)]
        w, h = v, v
        # создаем экземпляр QPainter, передавая холст (self.label.pixmap())
        painter = QPainter(self.ui.label.pixmap())
        pen = QPen()
        pen.setWidth(3)
        pen.setColor(QColor(*[randint(0, 255) for _ in range(3)]))
        painter.setPen(pen)
        painter.drawEllipse(x, y, w, h)
        painter.end()
        self.update()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = Test()
    ex.show()
    sys.exit(app.exec_())