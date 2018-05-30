#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui


class ItemGroup(QtGui.QGraphicsItemGroup):
    def __init__(self, scene, points):
        super(ItemGroup, self).__init__(parent=None, scene=scene)

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, True)
        self.setAcceptsHoverEvents(True)
        self.setSelected(False)

        self.setVisible(True)
        for p in points:
            self.addToGroup(p)

    def mousePressEvent(self, event):
        print("QGraphicsItemGroup mousePressEvent")
        # if self.scene().controller.current_group.get_id() == self.id:
        #     self.setSelected(True)
        # else:
        #     self.setSelected(False)

    def mouseReleaseEvent(self, event):
        print("QGraphicsItemGroup mouseReleaseEvent")
        #
        # if self.scene().controller.current_group.get_id() == self.id:
        #     self.setSelected(True)
        # else:
        #     self.setSelected(False)

    def get_id(self):
        return self.id

    def set_id(self, new_id):
        self.id = new_id
