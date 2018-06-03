#!/usr/bin/python
# -*- coding: utf-8 -*-

from Options import PointerMode
from PyQt4 import QtCore, QtGui
from PointGroup import PointGroup


class Controller(QtCore.QObject):
    create_new_item_group_signal = QtCore.pyqtSignal()
    delete_group_signal = QtCore.pyqtSignal(QtGui.QGraphicsItemGroup)
    update_scene_signal = QtCore.pyqtSignal()
    change_group_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)

        self.pointer_mode = PointerMode.INSERT_MODE
        self.item_groups = []
        self.max_group_id = 0
        self.current_group = None

    def update_scene(self):
        # self.current_group.update()
        self.current_group.update_group()
        self.update_scene_signal.emit()

    def delete_group(self, scene=None):
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

            self.item_groups.append(PointGroup(scene, group_id))

            if self.current_group is None:
                self.current_group = self.item_groups[-1]
            else:
                self.change_group(self.item_groups[-1].get_id())

    def add_item_to_group(self, point):
        self.current_group.add_point(point)

    def delete_point(self, item):
        self.current_group.delete_point(item)

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
        print("Change group to %s", group_id)
        self.current_group.set_flag(QtGui.QGraphicsItem.ItemIsMovable, False)
        self.current_group.set_flag(QtGui.QGraphicsItem.ItemIsFocusable, False)
        self.current_group.set_flag(QtGui.QGraphicsItem.ItemIsFocusable, False)

        for group in self.item_groups:
            if group.get_id() == group_id:
                self.current_group = group
                self.current_group.set_flag(QtGui.QGraphicsItem.ItemIsMovable, True)
                self.current_group.set_flag(QtGui.QGraphicsItem.ItemIsFocusable, True)
                self.current_group.set_flag(QtGui.QGraphicsItem.ItemIsFocusable, True)
                self.current_group.set_selected(True)
                break

        self.update_scene()
        self.change_group_signal.emit()

    def set_convex_hull(self, value):
        if value:
            self.current_group.draw_convex_hull()
        else:
            self.current_group.remove_convex_hull()
        self.update_scene()

    def change_curve(self, curve_id):
        self.current_group.change_curve(curve_id)

    def set_group_visible(self, value):
        self.current_group.set_visible(value)

    def is_group_visible(self):
        return self.current_group.is_group_visible()

    def merge_group(self, value):
        if value:
            self.current_group.merge()
        else:
            self.current_group.un_merge()
            self.update_scene()

    def get_pointer_mode(self):
        return self.pointer_mode

    def set_pointer_mode(self, mode):
        self.pointer_mode = mode
