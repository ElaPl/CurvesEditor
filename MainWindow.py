from PyQt4 import QtGui
from MainToolbar import MainToolbar


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.width = 1000
        self.height = 800
        self.setGeometry(0, 0, self.width, self.height)
        self.setWindowTitle("Curves editor")

        self.init_main_menu()
        self.init_toolbars()

    def init_toolbars(self):
        main_toolbar = MainToolbar(self)
        self.addToolBar(main_toolbar)

    def init_main_menu(self):
        main_menu = self.menuBar()

        new_action = QtGui.QAction("&Nowy", self)
        new_action.setShortcut("Ctrl+N")
        new_action.setStatusTip('Nowy plik')
        new_action.triggered.connect(self.new_file)

        file_menu = main_menu.addMenu('&Plik')
        file_menu.addAction(new_action)

        about_action = QtGui.QAction("&Informacje", self)
        about_action.setShortcut("Ctrl+I")
        about_action.setStatusTip('Pommoc')
        about_action.triggered.connect(self.show_info)

        file_menu = main_menu.addMenu('&Pomoc')
        file_menu.addAction(about_action)

    def new_file(self):
        print("New File")

    def show_info(self):
        print("Show Info")

    def save(self):
        print("Save")

    def open(self):
        print("Open")