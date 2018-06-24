#!/usr/bin/python
# -*- coding: utf-8 -*-

from ItemGroup import ItemGroup
from PyQt4 import QtCore
from ConvexHull import ConvexHull
from Options import CurveMode
from BezierCurve import BezierCurve
from BezierCurveHorner import BezierCurveHorner

class PointGroup(QtCore.QObject):

    def __init__(self, scene, group_id):
        super(PointGroup, self).__init__()
        print("New group id %s" % group_id)

        self.points = []
        self.scene = scene
        self.group_id = group_id
        self.is_visible = True
        self.is_merge = False
        self.merged_group = None
        self.convex_hull = None
        self.curve_id = CurveMode.NO_MODE
        self.curve = None

    def increase_degree_by_one(self):
        new_points = self.curve.increase_by_one()

        for p in self.points:
            self.scene.removeItem(p)
            if self.is_merge:
                self.merged_group.removeFromGroup(p)

        self.points = new_points

        for p in self.points:
            self.scene.addItem(p)
            if self.is_merge:
                self.merged_group.addToGroup(p)

        self.update_convex_hull()

    def decrease_degree_by_one(self):
        new_points = self.curve.decrease_by_one()

        for p in self.points:
            self.scene.removeItem(p)

        self.points = new_points

        for p in self.points:
            self.scene.addItem(p)

        self.update_convex_hull()

    def degree(self):
        if self.curve_id == CurveMode.NO_MODE :
            return len(self.points)
        else:
            return self.curve.get_degree()

    def change_curve(self, curve_id):
        if curve_id == CurveMode.NO_MODE and (self.curve is not None):
            self.curve_id = curve_id
            self.scene.removeItem(self.curve)
            if self.is_merge:
                self.merged_group.removeFromGroup(self.curve)

        else:
            if curve_id == CurveMode.BEZIER_CURVE:
                self.curve_id = curve_id
                new_curve = BezierCurve(self.points)
            if curve_id == CurveMode.BEZIER_CURVE_HORNER:
                self.curve_id = curve_id
                new_curve = BezierCurveHorner(self.points)
            if self.is_merge:
                if self.curve is not None:
                    self.merged_group.removeFromGroup(self.curve)
                self.merged_group.addToGroup(new_curve)
            else:
                if self.curve is not None:
                    self.scene.removeItem(self.curve)
                self.scene.addItem(new_curve)

            self.curve = new_curve

    def draw_convex_hull(self):
        self.convex_hull = ConvexHull(self.scene, self.points)
        if self.is_merge:
            self.merged_group.addToGroup(self.convex_hull)

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
            if self.curve_id != CurveMode.NO_MODE:
                self.curve.setSelected(value)
            if self.convex_hull is not None:
                self.convex_hull.setSelected(value)
        else:
            self.merged_group.setSelected(value)

    def set_flag(self, flag, value):
        if not self.is_merge:
            for p in self.points:
                p.setFlag(flag, value)
            if self.convex_hull is not None:
                self.convex_hull.setFlag(flag, value)
            if self.curve_id != CurveMode.NO_MODE:
                self.curve.setFlag(flag, value)
        else:
            self.merged_group.setFlag(flag, value)

    def get_id(self):
        return self.group_id

    def merge(self):
        other_list = []

        if self.convex_hull is not None:
            other_list.append(self.convex_hull)
        if self.curve_id != CurveMode.NO_MODE:
            other_list.append(self.curve)

        self.merged_group = ItemGroup(self, self.scene, self.points, other_list)
        self.is_merge = True
        self.merged_group.setSelected(True)

    def un_merge(self):
        self.scene.destroyItemGroup(self.merged_group)
        self.is_merge = False
        self.merged_group = None

    def set_visible(self, visible):
        self.is_visible = visible

        if self.is_merge:
            self.merged_group.setVisible(visible)
        else:
            for p in self.points:
                p.setVisible(visible)
            if self.convex_hull is not None:
                self.convex_hull.setVisible(visible)
            if self.curve_id != CurveMode.NO_MODE:
                self.curve.setVisible(visible)

    def is_group_visible(self):
        return self.is_visible

    def update_convex_hull(self):
        if self.convex_hull is not None:
            self.remove_convex_hull()
            self.draw_convex_hull()

    def update_bezier_curve(self):
        if self.curve_id != CurveMode.NO_MODE:
            self.curve.update_curve(self.points)

    def add_point(self, point):
        self.points.append(point)
        self.scene.addItem(point)

        self.update_convex_hull()

        if self.is_merge:
            self.merged_group.addToGroup(point)

        if self.curve_id != CurveMode.NO_MODE:
            self.curve.add_point(point)

    def delete_point(self, point):
        idx = 0
        for p in self.points:
            if p == point:
                del self.points[idx]
            idx += 1

        if self.is_merge:
            self.merged_group.removeFromGroup(point)
        else:
            self.scene.removeItem(point)

        self.update_convex_hull()
        self.curve.update_curve(self.points)

    def update_group(self):
        self.update_convex_hull()
        self.update_bezier_curve()
