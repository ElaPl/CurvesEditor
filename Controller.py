#!/usr/bin/python
# -*- coding: utf-8 -*-

from Options import PointerMode
from ItemGroup import ItemGroup
from PyQt4 import QtCore, QtGui


class Controller(QtCore.QObject):
    create_new_item_group_signal = QtCore.pyqtSignal()
    delete_group_signal = QtCore.pyqtSignal(QtGui.QGraphicsItemGroup)

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)

        self.pointer_mode = PointerMode.INSERT_MODE
        self.item_groups = []
        self.max_group_id = 0
        self.current_group = None

        self.elem_group_num = 1
        self.first_free_elem_group_id = 2

    def delete_group(self, scene=None):
        if scene is None:
            self.delete_group_signal.emit(self.current_group)
        else:
            self.item_groups.remove(self.current_group)
            if len(self.item_groups) == 0:
                self.new_item_group(scene)
            else:
                self.current_group = self.item_groups[0]

    def get_group_num(self):
        return len(self.item_groups)

    def new_item_group(self, scene=None, group_id=None):
        if scene is None:
            self.create_new_item_group_signal.emit()
        else:
            if group_id is None:
                self.max_group_id += 1
                group_id = "Group " + str(self.max_group_id)

            self.item_groups.append(ItemGroup(scene, group_id))
            self.current_group = self.item_groups[-1]

    def add_item_to_group(self, item):
        self.current_group.addToGroup(item)

    def remove_from_group(self, item):
        self.current_group.removeFromGroup(item)

    def get_group_id(self):
        return self.current_group.get_id()

    def set_group_id(self, new_id):
        self.current_group.set_id(new_id)

    def get_item_groups_id(self):
        groups_id = []
        for group in self.item_groups:
            groups_id.append(group.get_id())

        return groups_id

    def change_group(self, group_id):
        for group in self.item_groups:
            if group.get_id() == group_id:
                self.current_group = group
                break

    def get_pointer_mode(self):
        return self.pointer_mode

    def set_pointer_mode(self, mode):
        self.pointer_mode = mode
