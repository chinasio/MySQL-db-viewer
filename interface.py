from PyQt5 import QtCore

import pandas as pd


class PandasModel(QtCore.QAbstractTableModel):
    """

    """
    def __init__(self, df=pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df
        self._original_df = df.copy(deep=True)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """

        Parameters
        ----------
        section :
        orientation :
        role :

        Returns
        -------

        """
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """

        Parameters
        ----------
        index :
        role :

        Returns
        -------

        """
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()
        row = index.row()
        column = index.column()

        return QtCore.QVariant(str(self._df.ix[row, column]))

    def setData(self, index, value, role):
        """

        Parameters
        ----------
        index :
        value :
        role :

        Returns
        -------

        """
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            value = value.toPyObject()
        else:
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        """

        Parameters
        ----------
        column :
        order :

        Returns
        -------

        """
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

    def reset(self):
        # TODO
        self.layoutAboutToBeChanged.emit()
        self._df = self._original_df.copy(deep=True)
        self.layoutChanged.emit()

    def export(self, original=True):
        # TODO
        if original:
            self._original_df.to_excel('output.xlsx')
        else:
            self._df.to_excel('output_filtered.xlsx')

    def btn_clk(self):
        # TODO
        path = self.lineEdit.text()
        df = pd.read_csv(path)
        model = PandasModel(df)
        self.tableView.setModel(model)