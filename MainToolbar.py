from PyQt4 import QtGui


class MainToolbar(QtGui.QToolBar):
    def __init__(self, parent):
        super(MainToolbar, self).__init__(parent)
        self.setMovable(False)

        new = QtGui.QAction(QtGui.QIcon('images/new.png'), 'New', self)
        new.setShortcut('Ctrl+N')
        new.triggered.connect(self.parent().new_file)

        self.addAction(new)

        save = QtGui.QAction(QtGui.QIcon('images/save.png'), 'Save', self)
        save.setShortcut('Ctrl+S')
        save.triggered.connect(self.parent().save)

        self.addAction(save)

        open = QtGui.QAction(QtGui.QIcon('images/open.png'), 'Open', self)
        open.setShortcut('Ctrl+O')
        open.triggered.connect(self.parent().open)

        self.addAction(open)
