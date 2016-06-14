# -*- coding: utf-8 -*-
# This file is part of Python Boleto.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from babel.dates import format_date
from babel.numbers import format_currency


def format_agencia_conta(value):
    '''
    Formata numero de agencia e número de conta no formato: NNNN-D
    Obtém todos os números e considera o último como DV
    Uma string com 2 ou mais caracteres deve ser
    informado para que o formato seja aplicado
    '''

    if len(value) >= 2:
        return "{0}-{1}".format(value[:-1], value[-1])
    else:
        return value

def format_date_or_blank(value):
    if value:
        return format_date(value, format="dd/MM/yyyy", locale='pt_BR')
    return ""

def format_currency_or_blank(value):
    ''' Formata um valor decimal (dinheiro) ou retorna vazio '''
    if value:
        return format_currency(value, 'R$', locale='pt_BR')
    return ""

def index_or_blank(value, index):
    ''' Retorna um indice de uma lista se este existir ou vazio '''
    if len(value) > index:
        return value[index]

    return ""
