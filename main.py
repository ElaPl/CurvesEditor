#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from MainWindow import MainWindow


def start():
    if __name__ == '__main__':
        app = QtGui.QApplication(sys.argv)
        GUI = MainWindow()
        GUI.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    start()
