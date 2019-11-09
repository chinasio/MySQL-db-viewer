import mysql.connector
import db_setup
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

import pandas as pd

from interface import PandasModel


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=None)
        vLayout = QtWidgets.QVBoxLayout(self)
        hLayout = QtWidgets.QHBoxLayout()
        self.pathLE = QtWidgets.QLineEdit(self)
        hLayout.addWidget(self.pathLE)
        self.loadBtn = QtWidgets.QPushButton("Select File", self)
        self.exportBtn = QtWidgets.QPushButton("Export to File", self)
        self.exportFilteredBtn = QtWidgets.QPushButton("Export to File Filtered", self)
        self.filterLine = QtWidgets.QLineEdit(self)
        self.filterBtn = QtWidgets.QPushButton("Filter", self)

        hLayout.addWidget(self.loadBtn)
        hLayout.addWidget(self.exportBtn)
        hLayout.addWidget(self.exportFilteredBtn)
        hLayout.addWidget(self.filterLine)
        hLayout.addWidget(self.filterBtn)
        vLayout.addLayout(hLayout)
        self.pandasTv = QtWidgets.QTableView(self)
        vLayout.addWidget(self.pandasTv)
        self.loadBtn.clicked.connect(self.loadFile)
        self.exportBtn.clicked.connect(self.export)
        self.exportFilteredBtn.clicked.connect(lambda: self.export(False))
        self.filterBtn.clicked.connect(self.specify_filter)
        self.pandasTv.setSortingEnabled(True)

    def loadFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv)");
        self.pathLE.setText(fileName)
        df = pd.read_csv(fileName)
        model = PandasModel(df)
        self.pandasTv.setModel(model)

    def reset_filter(self):
        return self.pandasTv.model().reset()

    def specify_filter(self):
        options = self.filterLine.text()
        self.apply_filter(options)

    def setDf(self, df):
        model = PandasModel(df)
        self.pandasTv.setModel(model)

    def apply_filter(self, value=None):
        if not value:
            print("NOT A value")
            return self.pandasTv.model().reset()
        self.pandasTv.model().layoutAboutToBeChanged.emit()
        df = self.pandasTv.model()._original_df.copy(deep=True)
        df = df.query(value)
        self.pandasTv.model()._df = df
        self.pandasTv.model()._df.reset_index(inplace=True, drop=True)
        self.pandasTv.model().layoutChanged.emit()

    def export(self, original_df=True):
        filename = self.saveFileDialog()
        if not ('.xlsx' or '.xls') in filename:
            filename = filename + '.xlsx'
        writer = pd.ExcelWriter(filename,
                                engine='xlsxwriter')
        df = self.pandasTv.model()._original_df if original_df else self.pandasTv.model()._df
        df.to_excel(writer)
        writer.save()


    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Выгрузка таблицы", "", "Excel Files (*.xlsx)", options=options)
        return fileName


if __name__ == "__main__":
    cnx = mysql.connector.connect(**db_setup.grab_config())
    db_setup.db_start(cnx, db_setup.TABLES, db_setup.DB_NAME)
    db_setup.fill_in_db(cnx)
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.setDf(pd.read_sql(db_setup.grab_sql(), cnx))
    w.show()
    cnx.close()
    sys.exit(app.exec_())

