#!/usr/bin/python
# -*- coding: utf-8 -*-

from ItemGroup import ItemGroup
from PyQt4 import QtGui
from ConvexHull import ConvexHull

class PointGroup:
    def __init__(self, scene, group_id):
        print("New group id %s" % group_id)
        self.points = []
        self.scene = scene
        self.group_id = group_id
        self.is_visible = True
        self.is_merge = False
        self.merged_group = None
        self.convex_hull = None

    def draw_convex_hull(self):
        self.convex_hull = ConvexHull(self.scene, self.points)
        if self.is_merge:
            self.un_merge()
            self.merge()
            # self.merged_group.addToGroup(self.convex_hull)

    def remove_convex_hull(self):
        if self.convex_hull is not None:
            if self.is_merge:
                self.merged_group.removeFromGroup(self.convex_hull)
            self.scene.removeItem(self.convex_hull)
            self.convex_hull = None

    def set_selected(self, value):
        if not self.is_merge:
            for p in self.points:
                p.setSelected(value)
        else:
            self.merged_group.setSelected(value)

    def set_moveable(self, value):
        if not self.is_merge:
            for p in self.points:
                p.setFlag(QtGui.QGraphicsItem.ItemIsMovable, value)
        else:
            self.merged_group.setFlag(QtGui.QGraphicsItem.ItemIsMovable, value)

    def set_selectable(self, value):
        if not self.is_merge:
            for p in self.points:
                p.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, value)
        else:
            self.merged_group.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, value)

    def set_focusable(self, value):
        if not self.is_merge:
            for p in self.points:
                p.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, value)
        else:
            self.merged_group.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, value)

    def get_id(self):
        return self.group_id

    def merge(self):
        if self.convex_hull is not None:
            self.merged_group = ItemGroup(self.scene, self.points, [self.convex_hull])
        else:
            self.merged_group = ItemGroup(self.scene, self.points)
        self.is_merge = True
        self.merged_group.setSelected(True)

    def un_merge(self):
        self.scene.destroyItemGroup(self.merged_group)
        self.is_merge = False

    def set_visible(self, visible):
        self.is_visible = visible
        if self.convex_hull is not None:
            self.convex_hull.setVisible(visible)
        for p in self.points:
            p.setVisible(visible)
        if self.is_merge:
            self.merged_group.setVisible(visible)

    def is_group_visible(self):
        return self.is_visible

    def update_convex_hull(self):
        self.remove_convex_hull()
        self.draw_convex_hull()

    def add_point(self, point):
        self.points.append(point)
        if self.convex_hull is not None:
            self.update_convex_hull()
        if self.is_merge:
            self.merged_group.addToGroup(point)

    def delete_point(self, point):
        self.merged_group.removeFromGroup(point)
        if self.convex_hull is not None:
            self.update_convex_hull()
        idx = 0
        for p in self.points:
            if p == point:
                del self.points[idx]

            idx += 1

    def update(self):
        if self.convex_hull is not None:
            self.update_convex_hull()
