#!/usr/bin/python
# -*- coding: utf-8 -*-

from ItemGroup import ItemGroup


class PointGroup:
    def __init__(self, scene, group_id):
        print("New group id %s" % group_id)
        self.points = []
        self.scene = scene
        self.group_id = group_id
        self.is_visible = True
        self.is_merge = False
        self.merged_group = None

    def get_id(self):
        return self.group_id

    def merge(self):
        self.merged_group = ItemGroup(self.scene, self.points)
        self.is_merge = True

    def un_merge(self):
        self.scene.destroyItemGroup(self.merged_group)
        self.is_merge = False

    def set_visible(self, visible):
        self.is_visible = visible
        for p in self.points:
            p.setVisible(visible)
        if self.is_merge:
            self.merged_group.setVisible(visible)

    def is_group_visible(self):
        return self.is_visible

    def add_point(self, point):
        self.points.append(point)
        if self.is_merge:
            self.merged_group.addToGroup(point)

    def delete_point(self, point):
        self.merged_group.removeFromGroup(point)
        idx = 0
        for p in self.points:
            if p == point:
                del self.points[idx]

            idx += 1
