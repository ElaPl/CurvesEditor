#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from Options import PointerMode
from Point import Point


class DrawPanel(QtGui.QGraphicsScene):
    msg2Statusbar = QtCore.pyqtSignal(str)

    def __init__(self, width, height, controller, parent=None):
        super(DrawPanel, self).__init__(0, 0, width, height, parent)
        self.controller = controller
        self.controller.create_new_item_group_signal.connect(self.create_new_group)
        self.controller.delete_group_signal.connect(self.delete_group)
        self.controller.update_scene_signal.connect(self.update)
        self.controller.new_item_group()
        self.controller.new_item_group()

    def update(self):
        self.unselect_all_items()
        super(DrawPanel, self).update()

    def delete_group(self, group):
        self.destroyItemGroup(group)
        self.controller.delete_group(self)

    def create_new_group(self):
        self.controller.new_item_group(self)

    def drawBackground(self, painter, rect):
        self.setBackgroundBrush(QtCore.Qt.white)

        pen = QtGui.QPen(QtGui.QColor("grey"))
        pen.setWidth(1)
        painter.setPen(pen)

        line1 = QtCore.QLineF(0, 0, 0, self.height())
        line2 = QtCore.QLineF(0, self.height(), self.width(), self.height())
        line3 = QtCore.QLineF(self.width(), self.height(), self.width(), 0)
        line4 = QtCore.QLineF(self.width(), 0, 0, 0)
        painter.drawLines([line1, line2, line3, line4])

    def mousePressEvent(self, event):
        if PointerMode.INSERT_MODE == self.controller.get_pointer_mode() and \
                self.controller.is_group_visible():
            clickPoint = event.scenePos()
            if event.buttons() == QtCore.Qt.LeftButton:
                clickPoint = event.scenePos()
                if 0 < clickPoint.x() < self.width() and 0 < clickPoint.y() < self.height():
                    p = Point(clickPoint.x(), clickPoint.y(),
                              self.controller.get_group_id())
                    self.controller.add_item_to_group(p)
                    self.addItem(p)
                    # self.updateScene()
            else:
                item = self.itemAt(clickPoint)
                if item is not None and item.get_group_id() == self.controller.get_group_id():
                    self.removeItem(item)
                    if item is type(Point):
                        self.controller.delete_point(item)
                    # self.updateScene()

        super(DrawPanel, self).mousePressEvent(event)

    def unselect_all_items(self):
        for item in self.selectedItems():
            item.setSelected(False)

    def mouseMoveEvent(self, event):
        current_pos = event.scenePos()
        if 0 < current_pos.x() < self.width() and 0 < current_pos.y() < self.height():
            self.msg2Statusbar.emit('x: ' + str(current_pos.x()) + '  y: ' + str(current_pos.y()))
        super(DrawPanel, self).mouseMoveEvent(event)
