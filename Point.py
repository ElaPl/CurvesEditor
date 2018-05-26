#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from Options import PointerMode
from datetime import datetime


class Point(QtGui.QGraphicsItem):

    def __init__(self, x, y):
        super(Point, self).__init__(None)
        print("New point at: (%f, %f)" % (x, y))

        # self.parent = parent
        self.setPos(x, y)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, True)
        self.setAcceptsHoverEvents(True)

        self.brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        self.brush.setColor(QtCore.Qt.black)

        self.pen = QtGui.QPen(QtCore.Qt.SolidLine)
        self.pen.setWidth(2)
        self.pen.setColor(QtCore.Qt.black)
        self.pen.setBrush(self.brush)

        self.radius = 3
        self.creation_date = datetime.now()

    def boundingRect(self):
        return QtCore.QRectF(-self.radius, -self.radius, 2*self.radius, 2*self.radius)

    def paint(self, painter, option, widget=None):
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawEllipse(-self.radius, -self.radius, 2*self.radius, 2*self.radius)
        if self.isSelected():
            self.draw_focus_rect(painter)

    def draw_focus_rect(self, painter):
        focusbrush = QtGui.QBrush()
        focuspen = QtGui.QPen(QtCore.Qt.DotLine)
        focuspen.setColor(QtCore.Qt.black)
        focuspen.setWidthF(1)

        painter.setBrush(focusbrush)
        painter.setPen(focuspen)

        focus_rect = QtCore.QRectF(-self.radius-2, -self.radius-2, 2*self.radius+4,
                                   2*self.radius+4)
        painter.drawRect(focus_rect)

    def mouseMoveEvent(self, event):
        if self.scene().controller.get_pointer_mode() == PointerMode.EDIT_MODE:
            print("Point mouseMoveEvent")
            QtGui.QGraphicsItem.mouseMoveEvent(self, event)

            if self.scene().width() < self.x():
                self.setX(self.scene().width())
            if self.scene().height() < self.y():
                self.setY(self.scene().height())
            if self.y() < 0:
                self.setY(0)
            if self.x() < 0:
                self.setX(0)

            # self.scene().displayCoordinates(self.x(), self.y())
            # self.scene().updateScene()

    def mousePressEvent(self, event):
        print("Point mousePressEvent")
        if self.scene().controller.get_pointer_mode() == PointerMode.EDIT_MODE:
            self.setZValue(self.scene().items()[0].zValue() + 1)
            if event.buttons() == QtCore.Qt.LeftButton:
                self.scene().unselect_all_items()
            self.setSelected(True)
            # self.scene().displayCoordinates(self.x(), self.y())

            QtGui.QGraphicsItem.mousePressEvent(self, event)

    def hoverEnterEvent(self, event):
        self.brush.setColor(QtCore.Qt.blue)
        self.pen.setColor(QtCore.Qt.blue)
        QtGui.QGraphicsItem.hoverEnterEvent(self, event)

    def hoverLeaveEvent(self, event):
        self.brush.setColor(QtCore.Qt.black)
        self.pen.setColor(QtCore.Qt.black)
        QtGui.QGraphicsItem.hoverLeaveEvent(self, event)