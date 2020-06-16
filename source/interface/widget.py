from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
import pandas as pd
from source.interface.interface import PandasModel


class Widget(QtWidgets.QWidget):
    """
    Template class of QtWidgets.

    Parameters
    ----------
    parent : Qt.Widget object
        QtWidget to inherit it's properties
    """
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
        self.loadBtn.clicked.connect(self.load_file)
        self.exportBtn.clicked.connect(self.export)
        self.exportFilteredBtn.clicked.connect(lambda: self.export(False))
        self.filterBtn.clicked.connect(self.specify_filter)
        self.pandasTv.setSortingEnabled(True)

    def load_file(self):
        """
        Loading csv file with table's data and creating PandasModel instance of table.

        Returns
        -------
        None
        """
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv)");
        self.pathLE.setText(file_name)
        df = pd.read_csv(file_name)
        model = PandasModel(df)
        self.pandasTv.setModel(model)

    def reset_filter(self):
        """
        Method used to reset filters.

        Returns
        -------
        None
        """
        return self.pandasTv.model().reset()

    def specify_filter(self):
        """
        Determining type of filter.

        Returns
        -------
        None
        """
        options = self.filterLine.text()
        self.apply_filter(options)

    def set_df(self, df):
        """
        Method for creating PandasModel instance of table.

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame to be used for table's creation.
        Returns
        -------

        """
        model = PandasModel(df)
        self.pandasTv.setModel(model)

    def apply_filter(self, value=None):
        """
        Filter application method via PandasModel built-in methods.

        Parameters
        ----------
        value : str
            String of that contains pandas query.
        Returns
        -------
        None
        """
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
        """
        Exporting DataFrame to xls file.

        Parameters
        ----------
        original_df : pandas.DataFrame
            DataFrame to be exported.

        Returns
        -------
        None
        """
        filename = self.save_file_dialog()
        if not ('.xlsx' or '.xls') in filename:
            filename = filename + '.xlsx'
        writer = pd.ExcelWriter(filename,
                                engine='xlsxwriter')
        df = self.pandasTv.model()._original_df if original_df else self.pandasTv.model()._df
        df.to_excel(writer)
        writer.save()

    def save_file_dialog(self):
        """
        Function that determines behaviour of save button.

        Returns
        -------
        file_name : str
            Name of the saved file.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Выгрузка таблицы", "", "Excel Files (*.xlsx)", options=options)
        return file_name