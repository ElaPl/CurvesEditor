#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from Options import PointerMode


class ItemGroup(QtGui.QGraphicsItemGroup):
    def __init__(self, scene, points):
        super(ItemGroup, self).__init__(parent=None, scene=scene)

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptsHoverEvents(True)
        self.setSelected(False)

        self.setVisible(True)
        for p in points:
            self.addToGroup(p)

    def mouseMoveEvent(self, event):
        if self.scene().controller.get_pointer_mode() == PointerMode.EDIT_MODE:
            QtGui.QGraphicsItemGroup.mouseMoveEvent(self, event)

    def mousePressEvent(self, event):
        if self.scene().controller.get_pointer_mode() == PointerMode.EDIT_MODE:
            QtGui.QGraphicsItemGroup.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        if self.scene().controller.get_pointer_mode() == PointerMode.EDIT_MODE:
            QtGui.QGraphicsItemGroup.mouseReleaseEvent(self, event)

    def get_id(self):
        return self.id

    def set_id(self, new_id):
        self.id = new_id
