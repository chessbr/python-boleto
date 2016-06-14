# -*- coding: utf-8 -*-
# This file is part of Python Boleto.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.


def modulo10gen(num):
    ''' Generator para modulo 10: 2,1,2,1,2,1,2...'''

    current = 2
    while num > 0:
        yield current
        current = 1 if current == 2 else 2
        num = num - 1


def modulo11gen(num):
    ''' Generator para modulo 11: 2,3,4,5,6,7,8,9,2,3,4,5... '''

    current = 2
    while num > 0:
        yield current

        if current == 9:
            current = 2
        else:
            current = current + 1

        num = num - 1


def modulo10(value):
    '''
    Calcula o módulo 10 para o valor informado
    :type: value string
    :param: value Valor a ser obtido o múdulo 10, ex: 32361237
    '''

    algarismos = [int(a) for a in value if a.isdigit()]
    modulo10_multipliers = list(reversed(list(modulo10gen(len(algarismos)))))

    total = []
    for i in range(len(algarismos)):
        parcial = algarismos[i] * modulo10_multipliers[i]

        if parcial >= 10:
            # resultados com 9 digitos deve-se somar os 2 algarismos
            # ex: 15 -> 1+5 = 6   ou 15-9=6 
            parcial = parcial - 9 

        total.append(parcial)
    
    return 10 - (sum(total) % 10)


def modulo11(value):
    '''
    Calcula o módulo 11 para o valor informado
    :type: value string
    :param: value valor a ser obtido o módulo 11, ex: 38213216274752997
    '''
    algarismos = [int(a) for a in value if a.isdigit()]
    modulo11_multipliers = list(reversed(list(modulo11gen(len(algarismos)))))

    total = []
    for i in range(len(algarismos)):
        total.append(algarismos[i] * modulo11_multipliers[i])
        
    resto = sum(total) % 11

    # padrão é 1 quando resto for 0 ou 1
    if resto in (0, 1):
        return 1
    else:
    # se não for, o dv será 11-resto
        return 11 - resto
