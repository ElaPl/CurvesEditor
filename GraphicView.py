#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from DrawPanel import DrawPanel


class GraphicView(QtGui.QGraphicsView):

    def __init__(self, parent, width, height, controller, status_bar):
        super(GraphicView, self).__init__(parent)

        self.controller = controller
        self.status_bar = status_bar
        self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.HighQualityAntialiasing)
        self.setViewportUpdateMode(QtGui.QGraphicsView.FullViewportUpdate)

        self.draw_panel = self.new_graphic_scene(width, height)

    def new_graphic_scene(self, width, height):
        draw_panel = DrawPanel(width, height, self.controller, self)
        draw_panel.msg2Statusbar[str].connect(self.status_bar.showMessage)
        self.setScene(draw_panel)
        return draw_panel

    def update(self, *__args):
        self.draw_panel.unselect_all_items()
