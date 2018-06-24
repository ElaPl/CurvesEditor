#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from Options import PointerMode


class ItemGroup(QtGui.QGraphicsItemGroup):

    def __init__(self, parent, scene, points, other=None):
        QtGui.QGraphicsItemGroup.__init__(self, parent=None, scene=scene)

        self.parent = parent
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setAcceptsHoverEvents(True)
        self.setSelected(False)

        self.setVisible(True)
        for p in points:
            self.addToGroup(p)

        for elem in other:
            self.addToGroup(elem)

    def mouseMoveEvent(self, event):
        if self.scene().controller.get_pointer_mode() == PointerMode.EDIT_MODE:
            QtGui.QGraphicsItemGroup.mouseMoveEvent(self, event)

    def mousePressEvent(self, event):
        if self.scene().controller.get_pointer_mode() == PointerMode.EDIT_MODE:
            QtGui.QGraphicsItemGroup.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        if self.scene().controller.get_pointer_mode() == PointerMode.EDIT_MODE:
            QtGui.QGraphicsItemGroup.mouseReleaseEvent(self, event)
            self.parent.update_group()

    def get_id(self):
        return self.id

    def set_id(self, new_id):
        self.id = new_id
