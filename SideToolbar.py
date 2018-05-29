#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from Options import PointerMode


class SideToolbar(QtGui.QToolBar):
    def __init__(self, parent, controller):
        super(SideToolbar, self).__init__(parent)
        self.setMovable(True)
        self.controller = controller

        self.group_id_label = self.init_label()
        self.addSeparator()
        self.visible_check_box = self.init_visible_chekbox()

        #
        #
        # self.init_new_icon()
        # self.init_save_icon()
        # self.init_open_icon()
        #
        # self.addSeparator()
        # self.pointer_modes = self.init_pointer_modes()
        #
        # self.addSeparator()
        # self.item_groups_cb = self.init_group_item_cb()
        # self.init_new_group_icon()
        # self.init_delete_group_icon()

    def init_label(self):
        l1 = QtGui.QLabel(self.controller.current_group.get_id(), self)
        l1.setMargin(10)

        self.addWidget(l1)
        return l1

    def init_visible_chekbox(self):
        checkbox = QtGui.QCheckBox("Schowaj", self)
        checkbox.stateChanged.connect(self.hande_chenge_visible)

        self.addWidget(checkbox)
        return checkbox

    def init_connect_chekbox(self):
        checkbox = QtGui.QCheckBox("Schowaj", self)
        checkbox.stateChanged.connect(self.hande_chenge_visible)

        self.addWidget(checkbox)
        return checkbox


    def hande_chenge_visible(self):
        print("hande_chenge_visible handled")



    def init_new_group_icon(self):
        new_group = QtGui.QAction(QtGui.QIcon('images/add-icon.png'), 'New group', self)
        new_group.setShortcut('Ctrl+G')
        new_group.triggered.connect(self.add_new_group)

        self.addAction(new_group)

    def add_new_group(self):
        self.controller.new_item_group()
        self.update_item_group_cb(self.item_groups_cb)

    def init_delete_group_icon(self):
        delete_group = QtGui.QAction(QtGui.QIcon('images/delete-icon.png'), 'Delete group', self)
        delete_group.setShortcut('Ctrl+D')
        delete_group.triggered.connect(self.delete_group)

        self.addAction(delete_group)

    def delete_group(self):
        self.controller.delete_group()
        self.update_item_group_cb(self.item_groups_cb)

    def update_item_group_cb(self, cb):
        current_group_id = self.controller.current_group.get_id()
        groups_id = self.controller.get_item_groups_id()

        cb.clear()
        cb.addItems(groups_id)
        i = 0
        for id in groups_id:
            if id == current_group_id:
                break
            i += 1

        cb.setCurrentIndex(i)

    def init_group_item_cb(self):
        cb = QtGui.QComboBox()
        self.update_item_group_cb(cb)
        cb.currentIndexChanged.connect(self.handle_group_change)

        self.addWidget(cb)
        return cb

    def handle_group_change(self):
        self.controller.change_group(self.item_groups_cb.currentText())
        self.controller.update_side_toolbar(self.item_groups_cb.currentText())
        self.controller.update_scene()

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
