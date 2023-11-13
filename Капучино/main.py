import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel
from PyQt5.QtWidgets import QApplication, QMainWindow

db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('coffee.db')
db.open()


class AddWind(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        uic.loadUi("addEditCoffeeForm.ui", self)
        con = sqlite3.connect("coffee.db")
        cur = con.cursor()

        if Coffee.send == "Изменить":
            res = cur.execute(f"""SELECT * FROM Coffee WHERE ID = {Coffee.v}""").fetchone()
            self.name.setText(res[1])
            self.deg.setText(res[2])
            self.grind.setText(res[3])
            self.taste.setText(res[4])
            self.price.setText(str(res[5]))
            self.vol.setText(res[6])
        self.ok_btn.clicked.connect(self.update)
        self.show()

    def update(self):
        con = sqlite3.connect("coffee.db")
        cur = con.cursor()
        if Coffee.send == "Добавить":
            cur.execute(f"""INSERT
            INTO
            Coffee(
                name,
                degree,
                grind,
                taste,
                price,
                volume
            )
            VALUES(
                '{self.name.text()}',
                '{self.deg.text()}',
                '{self.grind.text()}',
                '{self.taste.text()}',
                {int(self.price.text())},
                '{self.vol.text()}'
            );""")
        else:
            cur.execute(f"""UPDATE Coffee SET
                            name = '{self.name.text()}',
                            degree = '{self.deg.text()}',
                            grind = '{self.grind.text()}',
                            taste = '{self.taste.text()}',
                            price = {int(self.price.text())},
                            volume = '{self.vol.text()}'
                            WHERE ID = {Coffee.v}""")
        con.commit()

        con.close()
        self.close()
        self.parent().update()


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        self.v = 0
        self.initUI()

    def initUI(self):
        uic.loadUi('main.ui', self)
        self.update()
        self.edit_btn.clicked.connect(self.on_click)
        self.add_btn.clicked.connect(self.on_click)

    def update(self):
        model = QSqlQueryModel()
        model.setQuery(f"""SELECT * FROM Coffee""")
        self.tableView.setModel(model)

    def on_click(self):
        Coffee.send = self.sender().text()

        if Coffee.send == "Изменить":
            try:
                Coffee.v = (self.tableView.selectionModel().currentIndex()).row() + 1

                self.add_form = AddWind(self)
            except AttributeError:
                self.statusBar().showMessage("Выберите объект из списка.")
        else:
            self.add_form = AddWind(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec())
