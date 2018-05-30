#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from MainToolbar import MainToolbar
from SideToolbar import SideToolbar
from GraphicView import GraphicView
from Controller import Controller


class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.width = 1000
        self.height = 800
        self.setGeometry(0, 0, self.width, self.height)
        self.setWindowTitle("Curves editor")

        self.controller = Controller()

        self.status_bar = self.statusBar()
        self.main_menu = self.init_main_menu()
        self.graphic_view = self.init_graphic_view()
        self.main_toolbar = self.init_main_toolbar()
        self.side_toolbar = self.init_side_toolbar()

        self.controller.change_group_signal.connect(self.handle_change_group)

    def handle_change_group(self):
        self.removeToolBar(self.side_toolbar)
        self.side_toolbar = self.init_side_toolbar()

    def update_scene(self):
        self.graphic_view.update()

    def init_graphic_view(self):
        graphic_view = GraphicView(self, self.width/2, self.height/2, self.controller,
                                   self.status_bar)
        self.setCentralWidget(graphic_view)
        return graphic_view

    def init_main_toolbar(self):
        main_toolbar = MainToolbar(self, self.controller)
        self.addToolBar(main_toolbar)
        return main_toolbar

    def init_side_toolbar(self):
        side_toolbar = SideToolbar(self, self.controller)
        self.addToolBar(QtCore.Qt.RightToolBarArea, side_toolbar)
        return side_toolbar

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
        return main_menu

    def new_file(self):
        print("New File")
        print(self.controller.get_pointer_mode())

    def show_info(self):
        print("Show Info")

    def save(self):
        print("Save")

    def open(self):
        print("Open")
