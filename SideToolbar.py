#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from Options import PointerMode, get_curve_names


class SideToolbar(QtGui.QToolBar):
    def __init__(self, parent, controller):
        super(SideToolbar, self).__init__(parent)
        self.setMovable(True)
        self.controller = controller

        self.group_id_label = self.init_label()
        self.addSeparator()
        self.visible_checkbox = self.init_visible_checkbox()
        self.merge_checkbox = self.init_merge_checkbox()
        self.addSeparator()
        self.convex_hull_checkbox = self.init_convex_hull_checkbox()
        # self.addSeparator()
        self.curve_combo_box = self.init_curve_combo_box()
        self.addSeparator()


    def init_curve_combo_box(self):
        cb = QtGui.QComboBox()
        cb.addItems(get_curve_names())
        cb.currentIndexChanged.connect(self.handle_change_curve)
        self.addWidget(cb)
        return cb

    def handle_change_curve(self):
        self.controller.change_curve(self.curve_combo_box.currentIndex())

    def init_convex_hull_checkbox(self):
        convex_hull_check_box = QtGui.QAction('Otoczka wypukła', self)
        convex_hull_check_box.setCheckable(True)
        convex_hull_check_box.setChecked(False)
        convex_hull_check_box.triggered.connect(self.handle_convex_hull_check)

        self.addAction(convex_hull_check_box)

        return convex_hull_check_box

    def handle_convex_hull_check(self):
        self.controller.set_convex_hull(self.convex_hull_checkbox.isChecked())

    def init_label(self):
        l1 = QtGui.QLabel(self.controller.current_group.get_id(), self)
        l1.setMargin(10)

        self.addWidget(l1)
        return l1

    def init_visible_checkbox(self):
        checkbox = QtGui.QCheckBox("Schowaj", self)
        if self.controller.current_group.is_group_visible():
            checkbox.setCheckState(0)
        else:
            checkbox.setCheckState(2)

        checkbox.stateChanged.connect(self.handle_change_visible)

        self.addWidget(checkbox)
        return checkbox

    def handle_change_visible(self):
        self.controller.set_group_visible(not self.visible_checkbox.isChecked())

    def init_merge_checkbox(self):
        checkbox = QtGui.QCheckBox("Scal", self)
        if self.controller.current_group.is_merge:
            checkbox.setCheckState(2)

        checkbox.stateChanged.connect(self.handle_change_merge_group)

        self.addWidget(checkbox)
        return checkbox

    def handle_change_merge_group(self):
        self.controller.merge_group(self.merge_checkbox.isChecked())
