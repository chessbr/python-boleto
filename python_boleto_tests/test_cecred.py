# -*- coding: utf-8 -*-
# This file is part of Python Boleto.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from python_boleto.cecred import CecredBoleto
import datetime
import pytest
from decimal import Decimal


def test_instantiate():
    cecred = CecredBoleto(**{'convenio':'123'})
    assert cecred.convenio == '123'


def test_validate():
    cecred = CecredBoleto()
    cecred.num_sequencial = 1
    cecred.vencimento = datetime.date.today()

    with pytest.raises(ValueError) as excinfo:
        cecred.validate()
    assert "convenio" in str(excinfo)

    cecred.convenio = '123'
    cecred.validate()


def test_nosso_numero():
    cecred = CecredBoleto()
    cecred.num_sequencial = 342
    cecred.conta_corrente = '7891'
    assert cecred.nosso_numero == "00007891000000342"


def test_fator_vencimento():
    cecred = CecredBoleto()

    # dentro do primeiro intervalo
    cecred.vencimento = datetime.date(2000, 7, 3)
    assert cecred.fator_vencimento == 1000
    cecred.vencimento = datetime.date(2000, 7, 4)
    assert cecred.fator_vencimento == 1001
    cecred.vencimento = datetime.date(2025, 2, 21)
    assert cecred.fator_vencimento == 9999

    # dentro do segundo intervalo
    cecred.vencimento = datetime.date(2025, 2, 22)
    assert cecred.fator_vencimento == 1000
    cecred.vencimento = datetime.date(2025, 2, 23)
    assert cecred.fator_vencimento == 1001

    # data muito baixa
    cecred.vencimento = datetime.date(1, 1, 1)
    assert cecred.fator_vencimento == 0

    # data muito alta
    cecred.vencimento = datetime.date(8978, 1, 1)
    assert cecred.fator_vencimento == 9999


def test_linha_digitavel():
    # Dados obtidos do boleto do manual da Cecred
    cecred = CecredBoleto()
    cecred.vencimento = datetime.date(2015, 5, 25)
    cecred.valor_documento = Decimal(1.00)
    cecred.convenio = '010120'
    cecred.conta_corrente = '03571572'
    cecred.num_sequencial = 1
    cecred.carteira = '1'
    assert cecred.linha_digitavel == "08590.10126 00357.157205 00000.001016 3 64390000000100"


def test_codigo_barras():
    # Dados obtidos do boleto do manual da Cecred
    # Lido representação do código de barras através da imagem
    cecred = CecredBoleto()
    cecred.vencimento = datetime.date(2015, 5, 25)
    cecred.valor_documento = Decimal(1.00)
    cecred.convenio = '010120'
    cecred.conta_corrente = '03571572'
    cecred.num_sequencial = 1
    cecred.carteira = '1'
    assert cecred.codigo_barras == "08593643900000001000101200357157200000000101"
    assert cecred.codigo_barras_dv == "3"
    
