from PyQt4 import QtGui, QtCore
from functools import reduce


class ConvexHull(QtGui.QGraphicsItem):
    def __init__(self, scene, points):
        super(ConvexHull, self).__init__(parent=None, scene=scene)
        self.pen = QtGui.QPen(QtCore.Qt.DotLine)
        self.pen.setWidth(1)
        self.pen.setColor(QtCore.Qt.black)

        if len(points) == 0:
            self.sortedPoints = []
            self.hullPoints = []

            self.boundingRect = QtCore.QRectF(0, 0, 0, 0)
        else:
            print("New convex")
            self.sortedPoints = sorted(points, key=lambda point: [point.x(), point.y()])
            self.hullPoints = self.convex_hull_graham()

            min_x = min([point.x() for point in self.sortedPoints])
            max_x = max([point.x() for point in self.sortedPoints])
            min_y = min([point.y() for point in self.sortedPoints])
            max_y = max([point.y() for point in self.sortedPoints])

            self.boundingRect = QtCore.QRectF(min_x, min_y, max_x - min_x + 2, max_y - min_y + 2)

    def boundingRect(self):
        return self.boundingRect

    def paint(self, painter, option, widget=None):
        if len(self.hullPoints) > 1:
            painter.setPen(self.pen)

            pointA = self.hullPoints[0]
            for point in self.hullPoints[1:]:
                # print("Print Line (%f, %f ) - (%f, %f )" %(pointA.x, pointA.y, point.x, point.y))
                painter.drawLine(pointA.x(), pointA.y(), point.x(), point.y())
                pointA = point

            painter.drawLine(pointA.x(), pointA.y(), self.hullPoints[0].x(), self.hullPoints[0].y())

    def convex_hull_graham(self):
        '''
        Returns points on convex hull in CCW order according to Graham's scan algorithm.
        '''

        # print("Computing conves hull of %d points " %(len(self.sortedPoints)))
        TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)

        def cmp(a, b):
            return (a > b) - (a < b)

        def turn(p, q, r):
            return cmp((q.x() - p.x()) * (r.y() - p.y()) - (r.x() - p.x()) * (q.y() - p.y()), 0)

        def _keep_left(hull, r):
            while len(hull) > 1 and turn(hull[-2], hull[-1], r) != TURN_LEFT:
                hull.pop()
            if not len(hull) or hull[-1] != r:
                hull.append(r)
            return hull

        points = self.sortedPoints
        l = reduce(_keep_left, points, [])
        u = reduce(_keep_left, reversed(points), [])
        return l.extend(u[i] for i in range(1, len(u) - 1)) or l

