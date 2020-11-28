from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5 import uic
from PyQt5 import QtCore
import sys
import sqlite3


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('main.ui', self)

        self.setWindowTitle('Кофе')
        self.setFixedSize(self.size())

        self.addButton.clicked.connect(self.open_form)
        self.redactButton.clicked.connect(self.open_form)

        self.connection = sqlite3.connect('coffee.sqlite')

        self.loadTable()

    def loadTable(self):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Название сорта', 'Степень обжарки', 'Вид',
                                                    'Описание вкуса', 'Цена (в рублях)', 'Объем упаковки (в граммах)'])
        res = self.connection.cursor().execute('SELECT * FROM coffee').fetchall()
        roast = dict(self.connection.cursor().execute('SELECT * FROM roast').fetchall())
        types = dict(self.connection.cursor().execute('SELECT * FROM type').fetchall())
        for i, content in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, cell in enumerate(content):
                if j == 2:
                    cell = roast[cell]
                elif j == 3:
                    cell = types[cell]
                ad = QTableWidgetItem(str(cell))
                ad.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, j, ad)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setCurrentCell(0, 1)

    def open_form(self):
        if self.sender().text() == 'Редактировать':
            data, r = [], self.tableWidget.currentRow()
            for i in range(1, 7):
                data.append(self.tableWidget.item(r, i).text())
            self.form = AddEditCoffeeForm(self, *data)
            self.form.show()
        else:
            self.form = AddEditCoffeeForm(self)
            self.form.show()


class AddEditCoffeeForm(QMainWindow):
    def __init__(self, parent, title='', roast='светлая', types='молотый', taste='', price='', volume=''):
        super().__init__()

        uic.loadUi('addEditCoffeeForm.ui', self)

        self.flag = 'add' if title == '' else 'update'

        self.parent = parent

        self.connection = sqlite3.connect('coffee.sqlite')
        self.cursor = self.connection.cursor()

        self.roast.addItems(['светлая', 'средняя', 'средне-темная', 'темная', 'очень темная'])
        self.types.addItems(['молотый', 'в зернах'])

        if self.flag == 'update':
            self.title.setText(title)
            self.title.setReadOnly(True)
            self.roast.setCurrentIndex(['светлая', 'средняя', 'средне-темная', 'темная', 'очень темная'].index(roast))
            self.types.setCurrentIndex(['молотый', 'в зернах'].index(types))
            self.taste.setPlainText(taste)
            self.price.setText(price)
            self.volume.setText(volume)

        self.confirmButton.clicked.connect(self.update_db)

    def update_db(self):
        try:
            title, roast, types, taste, price, volume = self.title.text(), self.roast.currentText(), \
                                                        self.types.currentText(), self.taste.toPlainText(), \
                                                        int(self.price.text()), int(self.volume.text())
            assert title
            assert taste

            r = dict(self.cursor.execute('SELECT title, id FROM roast').fetchall())
            t = dict(self.cursor.execute('SELECT title, id FROM type').fetchall())

            roast = r[roast]
            types = t[types]

            if self.flag == 'add':
                self.cursor.execute(f'''INSERT INTO coffee(title, roast, type, taste, price, volume) 
                VALUES("{title}", {roast}, {types}, "{taste}", {price}, {volume})''')
            else:
                self.cursor.execute(f'''UPDATE coffee 
SET roast = {roast}, type = {types}, price = {price}, volume = {volume}, taste = "{taste}" 
WHERE title = "{title}"''')

            self.connection.commit()
            QMessageBox.information(self, 'Успешно ', 'Таблица успешно обновлена', QMessageBox.Ok)
            self.connection.close()
            self.parent.loadTable()
            self.close()
        except AssertionError:
            QMessageBox.critical(self, 'Ошибка ', 'Введите название и описание', QMessageBox.Ok)
        except ValueError:
            QMessageBox.critical(self, 'Ошибка ', 'Введите числовые значения цены и объема', QMessageBox.Ok)
        except sqlite3.OperationalError:
            QMessageBox.critical(self, 'Ошибка ', 'Кофе с таким названием уже есть в базе', QMessageBox.Ok)


def main():
    app = QApplication(sys.argv)
    mw = MyWidget()
    mw.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
