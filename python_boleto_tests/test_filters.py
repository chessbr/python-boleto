# -*- coding: utf-8 -*-
# This file is part of Python Boleto.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import datetime
from decimal import Decimal

from python_boleto.filters import (
    format_agencia_conta, format_currency_or_blank, format_date_or_blank, index_or_blank
)


def test_format_agencia_conta():
    assert format_agencia_conta("12345") == "1234-5"
    assert format_agencia_conta("1234567890") == "123456789-0"
    assert format_agencia_conta("1") == "1"
    assert format_agencia_conta("") == ""

def test_format_date_or_blank():
    assert format_date_or_blank(datetime.date(2010, 1, 15)) == "15/01/2010"
    assert format_date_or_blank(None) == ""

def test_format_currency_or_blank():
    assert format_currency_or_blank(Decimal(1.59)) == "R$1,59"
    assert format_currency_or_blank(Decimal()) == ""
    assert format_currency_or_blank(None) == ""

def test_index_or_blank():
    assert index_or_blank(["a", "b", "c"], 2) == "c"
    assert index_or_blank(["a", "b", "c"], -1) == "c"
    assert index_or_blank(["a", "b", "c"], 3) == ""
