# -*- coding: utf-8 -*-
# This file is part of Python Boleto.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from python_boleto.utils import modulo10, modulo10gen, modulo11, modulo11gen


def test_modulo10gen():
    assert list(modulo10gen(5)) == [2,1,2,1,2]
    assert list(modulo10gen(10)) == [2,1,2,1,2,1,2,1,2,1]

def test_modulo11gen():
    assert list(modulo11gen(20)) == [2,3,4,5,6,7,8,9,2,3,4,5,6,7,8,9,2,3,4,5]
    assert list(modulo11gen(30)) == [2,3,4,5,6,7,8,9,2,3,4,5,6,7,8,9,2,3,4,5,6,7,8,9,2,3,4,5,6,7]

def test_modulo10():
    assert modulo10('01230067896') == 3
    assert modulo10('399983512') == 1
    assert modulo10('200002391') == 7
    assert modulo10('0476118682') == 6
    assert modulo10('085901012') == 6
    assert modulo10('0035715720') == 5
    assert modulo10('0000000101') == 6

def test_modulo11():
    assert modulo11('3999392300001200008351202000023910476118682') == 4
    assert modulo11('8220000215048200974123220154098290108605940') == 1
    assert modulo11('1049324200000321120055077222133347777777771') == 4
