import mysql.connector
import sys
from source.utilities import db_setup
from PyQt5 import QtWidgets
import pandas as pd
from source.interface.widget import Widget


if __name__ == "__main__":
    cnx = mysql.connector.connect(**db_setup.grab_config())
    db_setup.db_start(cnx, db_setup.TABLES, db_setup.DB_NAME)
    db_setup.fill_in_db(cnx)
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.set_df(pd.read_sql(db_setup.grab_sql(), cnx))
    w.show()
    cnx.close()
    sys.exit(app.exec_())

