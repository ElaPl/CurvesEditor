#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial

In this example, we create a simple
window in PyQt4.

author: Jan Bodnar
website: zetcode.com
last edited: October 2011
"""

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
