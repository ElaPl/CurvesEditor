#!/usr/bin/python
# -*- coding: utf-8 -*-

from Options import PointerMode


class Controller():
    def __init__(self):
        self.pointer_mode = PointerMode.INSERT_MODE

    def get_pointer_mode(self):
        return self.pointer_mode

    def set_pointer_mode(self, mode):
        self.pointer_mode = mode
