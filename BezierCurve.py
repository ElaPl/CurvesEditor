from PyQt4 import QtGui, QtCore
from Point import Point
import math

class simple_Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class BezierCurve(QtGui.QGraphicsItem):
    precision = 100

    def __init__(self, control_points):
        super(BezierCurve, self).__init__()
        self.controlPoints = control_points
        self.bezierPoints = self.computeBezierCurve(control_points)
        self.pen = QtGui.QPen(QtCore.Qt.SolidLine)
        self.pen.setWidth(2)
        self.pen.setColor(QtCore.Qt.blue)

        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)
        # self.setFlag(QtGui.QGraphicsItem.ItemIsPanel, False)
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, False)

    def get_degree(self):
        return len(self.controlPoints) - 1

    def increase_by_one(self):
        curr_degree = len(self.controlPoints)
        group_id = self.controlPoints[0].group_id

        new_control_points = []
        first_point = Point(self.controlPoints[0].x(), self.controlPoints[0].y(), group_id)
        new_control_points.append(first_point)

        for i in range(1, curr_degree):
            x = i/(curr_degree + 1) * self.controlPoints[i-1].x() + \
                (curr_degree + 1 - i) / (curr_degree + 1) * self.controlPoints[i].x()
            y = i / (curr_degree + 1) * self.controlPoints[i - 1].y() + \
                (curr_degree + 1 - i) / (curr_degree + 1) * self.controlPoints[i].y()

            new_control_points.append(Point(x, y, group_id))

        last_point = Point(self.controlPoints[curr_degree - 1].x(),
                           self.controlPoints[curr_degree - 1].y(), group_id)

        new_control_points.append(last_point)
        self.controlPoints = new_control_points
        self.bezierPoints = self.computeBezierCurve(self.controlPoints)
        self.update()
        return self.controlPoints

    def decrease_by_one(self):
        curr_degree = len(self.controlPoints)
        if curr_degree < 4:
            return self.controlPoints

        group_id = self.controlPoints[0].group_id
        half_idx = math.floor(curr_degree/2)

        new_control_points = []
        first_point = Point(self.controlPoints[0].x(), self.controlPoints[0].y(), group_id)
        new_control_points.append(first_point)

        for i in range(1, half_idx):
            x = (curr_degree/(curr_degree - i)) * self.controlPoints[i].x() - \
                (i/(curr_degree - i)) * new_control_points[i-1].x()
            y = (curr_degree/(curr_degree - i)) * self.controlPoints[i].y() - \
                (i/(curr_degree - i)) * new_control_points[i-1].y()

            new_control_points.append(Point(x, y, group_id))

        print("new contro points : len: ", len(new_control_points))
        # new_control_points.append(Point(self.controlPoints[half_idx].x(),
        #                                 self.controlPoints[half_idx].y(),
        #                                 group_id))

        last_point = Point(self.controlPoints[curr_degree - 1].x(),
                           self.controlPoints[curr_degree - 1].y(), group_id)

        new_control_points_2 = []
        new_control_points_2.append(last_point)

        it = 0
        for i in range(curr_degree - 2, half_idx - 1, -1):
            x = (curr_degree/i) * self.controlPoints[i].x() - \
                ((curr_degree - i)/i) * new_control_points_2[it].x()
            y = (curr_degree/i) * self.controlPoints[i].y() - \
                ((curr_degree - i)/i) * new_control_points_2[it].y()
            it = it + 1

            new_control_points_2.append(Point(x, y, group_id))

        new_control_points_2.reverse()

        if new_control_points[-1] != new_control_points_2[0]:
            new_control_points_3 = new_control_points[0:-1]
            print(len(new_control_points_3))
            x = 1/2 * new_control_points[-1].x() + 1/2 * new_control_points_2[0].x()
            y = 1/2 * new_control_points[-1].y() + 1/2 * new_control_points_2[0].y()
            new_control_points_3.append(Point(x, y, group_id))
            print(len(new_control_points_3))
            new_control_points_3.extend(new_control_points_2[1:])
            print(len(new_control_points_3))
            self.controlPoints = new_control_points_3
        else:
            self.controlPoints = new_control_points
            self.controlPoints.extend(new_control_points_2[1:])

        self.bezierPoints = self.computeBezierCurve(self.controlPoints)
        self.update()
        return self.controlPoints

    def add_point(self, point):
        self.controlPoints.append(point)
        self.bezierPoints = self.computeBezierCurve(self.controlPoints)
        self.update()

    def computeBezierCurve(self, controlPoints):
        controlPointsNum = len(controlPoints)
        if controlPointsNum < 2:
            return []

        bezierPoints = []
        bezierPoints.append(simple_Point(controlPoints[0].x(), controlPoints[0].y()))

        if controlPointsNum > 2:
            for i in range(1, self.precision):
                bezierPoints.append(self.deCasteliau(controlPoints, controlPointsNum, i / self.precision))

        bezierPoints.append(simple_Point(controlPoints[-1].x(), controlPoints[-1].y()))
        return bezierPoints

    def deCasteliau(self, controlPoints, controlPointsNum, u):
        values = [[]]
        for i in range(0, controlPointsNum):
            values[0].append(simple_Point(controlPoints[i].x(), controlPoints[i].y()))

        for i in range(1, controlPointsNum):
            row = []
            for j in range(0, controlPointsNum - i):
                x = (1 - u) * values[i - 1][j].x + u * values[i - 1][j + 1].x
                y = (1 - u) * values[i - 1][j].y + u * values[i - 1][j + 1].y
                row.append(simple_Point(x, y))
            values.append(row)

        return values[controlPointsNum - 1][0]

    def boundingRect(self):
        if len(self.bezierPoints) > 0:
            leftX = min([point.x for point in self.bezierPoints])
            rightX = max([point.x for point in self.bezierPoints])
            maxY = max([point.y for point in self.bezierPoints])
            minY = min([point.y for point in self.bezierPoints])

            return QtCore.QRectF(leftX, minY, rightX - leftX, maxY - minY)
        return QtCore.QRectF(0, 0, 0, 0)

    def paint(self, painter, option, widget=None):
        painter.setPen(self.pen)
        bezierPointsNum = len(self.bezierPoints)
        for i in range(0, bezierPointsNum - 1):
            painter.drawLine(self.bezierPoints[i].x, self.bezierPoints[i].y,
                             self.bezierPoints[i + 1].x, self.bezierPoints[i + 1].y)

    def update_curve(self, control_points):
        self.controlPoints = control_points
        self.bezierPoints = self.computeBezierCurve(self.controlPoints)
        self.update()
