#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from Options import PointerMode


class MainToolbar(QtGui.QToolBar):
    def __init__(self, parent, controller):
        super(MainToolbar, self).__init__(parent)
        self.setMovable(False)
        self.controller = controller

        self.init_new_icon()
        self.init_save_icon()
        self.init_open_icon()

        self.addSeparator()
        self.pointer_modes = self.init_pointer_modes()

    def init_pointer_modes(self):
        insert_mode = QtGui.QAction(QtGui.QIcon('images/action.png'), 'Insert mode', self)
        insert_mode.setShortcut('Ctrl+I')
        insert_mode.triggered.connect(lambda: self.pointer_mode_toggle(PointerMode.INSERT_MODE))
        insert_mode.setIconVisibleInMenu(True)

        if self.controller.get_pointer_mode() == PointerMode.INSERT_MODE:
            insert_mode.setVisible(False)
        else:
            insert_mode.setVisible(True)

        self.addAction(insert_mode)

        edit_mode = QtGui.QAction(QtGui.QIcon('images/editIcon.png'), 'Edit mode', self)
        edit_mode.setShortcut('Ctrl+E')
        edit_mode.triggered.connect(lambda: self.pointer_mode_toggle(PointerMode.EDIT_MODE))
        edit_mode.setIconVisibleInMenu(True)

        if self.controller.get_pointer_mode() == PointerMode.EDIT_MODE:
            edit_mode.setVisible(False)
        else:
            edit_mode.setVisible(True)

        self.addAction(edit_mode)

        return [insert_mode, edit_mode]

    def pointer_mode_toggle(self, mode):
        self.controller.set_pointer_mode(mode)

        for mode in self.pointer_modes:
            mode.setVisible((not mode.isVisible()))

    def init_new_icon(self):
        new = QtGui.QAction(QtGui.QIcon('images/new.png'), 'New', self)
        new.setShortcut('Ctrl+N')
        new.triggered.connect(self.parent().new_file)

        self.addAction(new)

    def init_save_icon(self):
        save = QtGui.QAction(QtGui.QIcon('images/save.png'), 'Save', self)
        save.setShortcut('Ctrl+S')
        save.triggered.connect(self.parent().save)

        self.addAction(save)

    def init_open_icon(self):
        open = QtGui.QAction(QtGui.QIcon('images/open.png'), 'Open', self)
        open.setShortcut('Ctrl+O')
        open.triggered.connect(self.parent().open)

        self.addAction(open)
