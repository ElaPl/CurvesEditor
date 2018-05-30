#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui


class ItemGroup(QtGui.QGraphicsItemGroup):
    def __init__(self):
        super(ItemGroup, self).__init__()

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, True)
        self.setAcceptsHoverEvents(True)
        self.setSelected(False)

        self.setVisible(True)

    def mousePressEvent(self, event):
        print("QGraphicsItemGroup mousePressEvent")
        if self.scene().controller.current_group.get_id() == self.id:
            self.setSelected(True)
        else:
            self.setSelected(False)

    def mouseReleaseEvent(self, event):
        print("QGraphicsItemGroup mouseReleaseEvent")

        if self.scene().controller.current_group.get_id() == self.id:
            self.setSelected(True)
        else:
            self.setSelected(False)

    def get_id(self):
        return self.id

    def set_id(self, new_id):
        self.id = new_id
