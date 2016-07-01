# -*- coding: utf-8 -*-
# This file is part of Python Boleto.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from python_boleto.base import Boleto


def test_base_not_implemented():
    base = Boleto()

    with pytest.raises(NotImplementedError):
        base.nosso_numero()

    with pytest.raises(NotImplementedError):
        base.linha_digitavel()

    with pytest.raises(NotImplementedError):
        base.codigo_barras_dv()

    with pytest.raises(NotImplementedError):
        base.codigo_barras()

    assert base.get_context_data() is None

def test_base_validate():
    base = Boleto()

    # num_sequencial
    base.num_sequencial = ''
    assert base.num_sequencial == 0

    base.num_sequencial = -1
    with pytest.raises(ValueError) as excinfo:
        base.validate()
    assert "num_sequencial" in str(excinfo)
    base.num_sequencial = 1

    # quantidade
    base.quantidade = ''
    assert base.quantidade == 0

    base.quantidade = -1
    with pytest.raises(ValueError) as excinfo:
        base.validate()
    assert "quantidade" in str(excinfo)
    base.quantidade = 0

    # vencimento
    with pytest.raises(TypeError) as excinfo:
        base.validate()
    assert "vencimento" in str(excinfo)
    base.vencimento = datetime.now().date()


    # data_documento
    base.data_documento = -1
    with pytest.raises(TypeError) as excinfo:
        base.validate()
    assert "data_documento" in str(excinfo)
    base.data_documento = datetime.now()

    # data_processamento
    base.data_processamento = -1
    with pytest.raises(TypeError) as excinfo:
        base.validate()
    assert "data_processamento" in str(excinfo)
    base.data_processamento = datetime.now()

    # valor_unitario
    base.valor_unitario = -1
    assert base.valor_unitario == Decimal(-1)
    base.valor_unitario = Decimal()

    # valor_documento
    base.valor_documento = -1
    assert base.valor_documento == Decimal(-1)
    base.valor_documento = Decimal()

    # valor_desconto
    base.valor_desconto = -1
    assert base.valor_desconto == Decimal(-1)
    base.valor_desconto = Decimal()

    # valor_outras_deducoes
    base.valor_outras_deducoes = -1
    assert base.valor_outras_deducoes == Decimal(-1)
    base.valor_outras_deducoes = Decimal()

    # valor_multa
    base.valor_multa = -1
    assert base.valor_multa == Decimal(-1)
    base.valor_multa = Decimal()

    # valor_outros_acrescimos
    base.valor_outros_acrescimos = -1
    assert base.valor_outros_acrescimos == Decimal(-1)
    base.valor_outros_acrescimos = Decimal()

    # valor_cobrado
    base.valor_cobrado = -1
    assert base.valor_cobrado == Decimal(-1)
    base.valor_cobrado = Decimal()

    # numero_documento
    base.numero_documento = -1
    assert base.numero_documento == '-1'

    # especie_documento
    base.especie_documento = -1
    assert base.especie_documento == '-1'

    # aceite
    base.aceite = -1
    assert base.aceite == '-1'

    # especie
    base.especie = -1
    assert base.especie == '-1'

    # sacado
    base.sacado = -1
    assert base.sacado == '-1'

    # cpf_cei_cnpj
    base.cpf_cei_cnpj = -1
    assert base.cpf_cei_cnpj == '-1'

    # sacador_avalista
    base.sacador_avalista = -1
    assert base.especie == '-1'

    # local_pagamento
    base.local_pagamento = -1
    assert base.local_pagamento == '-1'

    # cedente
    base.cedente = -1
    assert base.cedente == '-1'

    # agencia
    base.agencia = -1
    assert base.agencia == '-1'

    # conta_corrente
    base.conta_corrente = -1
    assert base.especie == '-1'

    # carteira
    base.carteira = -1
    assert base.especie == '-1'

    # contrato
    base.contrato = -1
    assert base.especie == '-1'

    # instrucoes
    base.instrucoes = -1
    with pytest.raises(TypeError) as excinfo:
        base.validate()
    assert "instrucoes" in str(excinfo)
    base.instrucoes = []

    # informacoes
    base.informacoes = -1
    with pytest.raises(TypeError) as excinfo:
        base.validate()
    assert "informacoes" in str(excinfo)
    base.informacoes = []

    # sacado_extra
    base.sacado_extra = -1
    with pytest.raises(TypeError) as excinfo:
        base.validate()
    assert "sacado_extra" in str(excinfo)
    base.sacado_extra = []


def test_instantiate_and_export_html():
    boleto_info = {"vencimento": datetime.today() + timedelta(days=10)}
    base = Boleto(**boleto_info)
    html = base.export_html(static_url="https://static.mydomain.com/")
    assert html == "<html></html>"
