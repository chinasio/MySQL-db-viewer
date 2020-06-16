import pandas as pd
from PyQt5 import QtCore


class PandasModel(QtCore.QAbstractTableModel):
    """
    Model that allow to represent pandas DataFrame as QtTable.

    Arguments
    ----------
    df : pandas.DataFrame
        DataFrame to be table initiated with.
    parent : bool
        Optional built-in method in QtCore to inherit properties of similar Qt object.
    """
    def __init__(self, df=pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df
        self._original_df = df.copy(deep=True)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """


        Parameters
        ----------
        section : str
            Section of DataFrame to take headers from.
        orientation : QtCore.Qt object
            One of Qt attributes that determine table orientation via headers placements
            (horizontal or vertical).
        role : QtCore.Qt object
            Parameter that responsible for choosing if data to be rendered visually as QString.

        Returns
        -------
        None
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
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """

        Parameters
        ----------
        index : pandas.DataFrame.index
            Index of DataFrame for table to be rendered.
        role : QtCore.Qt object
            Parameter that responsible for choosing if data to be rendered visually as QString.

        Returns
        -------
        QtCore.QVariant
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
        index : pandas.DataFrame.index
            Index of DataFrame for table to be rendered.
        value : str
            Values to be added to table.
        role : QtCore.Qt object
            Parameter that responsible for choosing if data to be rendered visually as QString.

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
        Implementation of excel-like column sorting via built-in Qt methods.

        Parameters
        ----------
        column : pandas.DataFrame
            Using pandas columns attribute to get list of columns.
        order : QtCore.Qt.AscendingOrder
            Qt built-in attribute to set oder of table's columns sort.
        Returns
        -------
        None
        """
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending=order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

    def reset(self):
        # Implementation of method that allow to go back to original df,
        # in sense of resetting used filters.
        self.layoutAboutToBeChanged.emit()
        # just reassign self._df to original
        self._df = self._original_df.copy(deep=True)
        self.layoutChanged.emit()

    def export(self, original=True):
        # Outputting to excel file via DataFrame in-built method.
        if original:
            self._original_df.to_excel('output.xlsx')
        else:
            self._df.to_excel('output_filtered.xlsx')

    def btn_clk(self):
        # Method that defines behaviour of import button.
        path = self.lineEdit.text()
        df = pd.read_csv(path)
        model = PandasModel(df)
        self.tableView.setModel(model)