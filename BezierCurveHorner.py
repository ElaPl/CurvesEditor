from PyQt4 import QtGui, QtCore
# from Curve import Curve

class simple_Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class BezierCurveHorner(QtGui.QGraphicsItem):
    precision = 100

    def __init__(self, control_points):
        super(BezierCurveHorner, self).__init__(parent=None)
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
                bezierPoints.append(self.horner(controlPoints, controlPointsNum,
                                               i / self.precision))

        bezierPoints.append(simple_Point(controlPoints[-1].x(), controlPoints[-1].y()))
        return bezierPoints

    def horner(self, controlPoints, controlPointsNum, t):
        x = controlPoints[0].x()
        y = controlPoints[0].y()
        s = 1 - t
        d = t
        b = controlPointsNum
        for i in range(1, controlPointsNum):
            x += s * x + b * d * self.controlPoints[i].x()
            y += s * y + b * d * self.controlPoints[i].y()
            d = d * t
            b = b * (controlPointsNum - i) / (i + 1)
        return simple_Point(x, y)

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
