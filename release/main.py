import sys
import sqlite3
from PyQt5.QtWidgets import *

from release.addEditCoffeeForm import Ui_Form
from release.mainui import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("data/coffee.sqlite")
        self.load_table()

        self.btn_add.clicked.connect(self.add)
        self.btn_edit.clicked.connect(self.edit)

    def load_table(self):
        self.tableWidget.clear()
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        titles = [description[0] for description in cur.description]
        self.tableWidget.setHorizontalHeaderLabels(titles)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def add(self):
        self.form = AddForm(self)
        self.form.show()

    def edit(self):
        cur = self.con.cursor()
        index = self.tableWidget.selectedIndexes()
        if not index:
            return
        id = int(self.tableWidget.item(index[0].row(), 0).text())
        mas = cur.execute("""SELECT * FROM coffee WHERE id == ?""", (id,)).fetchone()
        self.form = EditForm(self, mas)
        self.form.show()

    def add_new(self, name, roast, ground, price, volume, des):
        cur = self.con.cursor()
        id = cur.execute('SELECT id from coffee').fetchall()
        cur.execute('INSERT INTO coffee VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (sorted(id)[-1][0] + 1, name, roast, ground, price, volume, des))
        self.con.commit()
        self.load_table()

    def edit_new(self, name, roast, ground, price, volume, des, id):
        cur = self.con.cursor()
        cur.execute("UPDATE coffee SET name = ?, roasting = ?, ground_or_in_grains = ?, "
                    "price = ?, volume = ?, description = ? WHERE id = ?",
                    (name, roast, ground, price, volume, des, id))
        self.con.commit()
        self.load_table()


class AddForm(QWidget, Ui_Form):
    def __init__(self, main):
        super().__init__()
        self.setupUi(self)
        self.main = main
        self.setWindowTitle('Добавление')
        self.pushButton.clicked.connect(self.run)

    def run(self):
        self.main.add_new(self.name_line.text(), self.roast_line.text(), self.ground_line.text(),
                          self.price_line.text(), self.volume_line.text(), self.des_line.text())
        self.close()


class EditForm(QWidget, Ui_Form):
    def __init__(self, main, mas):
        super().__init__()
        self.setupUi(self)
        self.main = main
        self.id = mas[0]
        self.setWindowTitle('Редактирование')
        self.pushButton.clicked.connect(self.run)

        self.name_line.setText(mas[1])
        self.roast_line.setText(mas[2])
        self.ground_line.setText(mas[3])
        self.price_line.setText(str(mas[4]))
        self.volume_line.setText(str(mas[5]))
        self.des_line.setText(mas[6])

    def run(self):
        self.main.edit_new(self.name_line.text(), self.roast_line.text(), self.ground_line.text(),
                           self.price_line.text(), self.volume_line.text(), self.des_line.text(), self.id)
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
