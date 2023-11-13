import sys

from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel
from PyQt5.QtWidgets import QApplication, QMainWindow

db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('coffee.db')
db.open()


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('main.ui', self)
        model = QSqlQueryModel()
        model.setQuery(f"""SELECT * FROM Coffee""")
        self.tableView.setModel(model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec())
