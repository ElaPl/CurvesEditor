from PyQt4 import QtGui, QtCore
# from Curve import Curve

class simple_Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class BezierCurve(QtGui.QGraphicsItem):
    precision = 1000

    def __init__(self, control_points, scene):
        super(BezierCurve, self).__init__(parent=None, scene=scene)
        self.controlPoints = control_points
        self.bezierPoints = self.computeBezierCurve(control_points)
        self.pen = QtGui.QPen(QtCore.Qt.SolidLine)
        self.pen.setWidth(2)
        self.pen.setColor(QtCore.Qt.blue)

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
        leftX = min([point.x for point in self.bezierPoints])
        rightX = max([point.x for point in self.bezierPoints])
        maxY = max([point.y for point in self.bezierPoints])
        minY = min([point.y for point in self.bezierPoints])

        return QtCore.QRectF(leftX, minY, rightX - leftX, maxY - minY)

    def paint(self, painter, option, widget=None):
        painter.setPen(self.pen)
        bezierPointsNum = len(self.bezierPoints)
        for i in range(0, bezierPointsNum - 1):
            painter.drawLine(self.bezierPoints[i].x, self.bezierPoints[i].y,
                             self.bezierPoints[i + 1].x, self.bezierPoints[i + 1].y)
