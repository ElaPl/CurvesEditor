#!/usr/bin/python
# -*- coding: utf-8 -*-


class PointerMode:
    INSERT_MODE = 1
    EDIT_MODE = 2

class CurveMode:
    NO_MODE = 0
    BEZIER_CURVE = 1 << 0
    BEZIER_CURVE_HORNER = 1 << 1


curve_options = [("No curve", CurveMode.NO_MODE),
                 ("Bezier curve", CurveMode.BEZIER_CURVE)]
                 # ("Bezier curve horner", CurveMode.BEZIER_CURVE_HORNER)]

def get_curve_names():
    l = []
    for name, num in curve_options:
        l.append(name)

    return l