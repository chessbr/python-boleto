# -*- coding: utf-8 -*-
# This file is part of Python Boleto.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from datetime import date
from decimal import Decimal

from python_boleto.base import Boleto
from python_boleto.utils import modulo10, modulo11
import six


class CecredBoleto(Boleto):
    _banco = '085'
    _template = 'cecred.jinja'
    _logo = 'cecred.jpg'

    # numero do convenio
    convenio = ''

    @property
    def nosso_numero(self):
        '''
        É composto por 17 dígitos incluindo o dígito verificador
        da conta corrente e, deve ser gerado por meio de sequenciais
        diferentes, não podendo retroagir ou repetir numeração já processada,
        utiliza-se o número do boleto como critério sequencial.
        Sugere-se a emissão em produção pelo boleto no 1.
        O quadro abaixo explica como compor este campo:
            - 8 primeiros dígitos: Conta corrente + dv do cooperado (Sempre será fixo)
            - 9 dígitos restantes: Número do boleto (Sequencial)
        '''
        conta = "{:0>8}".format("".join([d for d in self.conta_corrente if d.isdigit()])[:8])
        numero = "{:0>9}".format(self.num_sequencial)
        return conta + numero

    @property
    def fator_vencimento(self):
        '''
        - Para vencimento até 21/02/2025 deverá ser utilizada a data base de 07.10.1997, calculando o
        número de dias entre essa data e a do vencimento (data de vencimento menos data base = fator)
        - A partir do dia 22/02/2025 deverá ser considerado a sequência de um novo fator com
        numeração 1000.
        '''
        fator = 0

        if self.vencimento <= date(2025, 2, 21):
            fator = (self.vencimento - date(1997, 10, 7)).days
        else:
            fator = (self.vencimento - date(2025, 2, 22)).days + 1000

        # deixa no intervalo (0, 9999)
        return max(0, min(fator, 9999))

    @property
    def linha_digitavel(self):
        linha_total_fmt = "{banco}{moeda}{convenio}{conta_corrente}"\
                          "{num_sequencial}{carteira}{fator_vencto}{valor}"

        valor = str(int(self.valor_documento * Decimal(100.0)))

        linha_total = linha_total_fmt.format(**{'banco': "{:0>3}".format(self._banco)[-3:],
                                                'moeda': '9',
                                                'convenio': "{:0>6}".format(self.convenio)[-6:],
                                                'conta_corrente': "{:0>8}".format(self.conta_corrente)[-8:],
                                                'num_sequencial': "{:0>9}".format(self.num_sequencial)[-9:],
                                                'carteira': "{:0>2}".format(self.carteira)[-2:],
                                                'fator_vencto': "{:0>4}".format(self.fator_vencimento)[-4:],
                                                'valor': "{:0>10}".format(valor)[-10:]})

        campo1 = linha_total[:9]
        campo2 = linha_total[9:19]
        campo3 = linha_total[19:29]
        campo4 = str(self.codigo_barras_dv)
        campo5 = linha_total[-14:]

        # formata e calcula os DAC com modulo10
        campo1 = "{0}.{1}{2}".format(campo1[:5], campo1[5:], modulo10(campo1))
        campo2 = "{0}.{1}{2}".format(campo2[:5], campo2[5:], modulo10(campo2))
        campo3 = "{0}.{1}{2}".format(campo3[:5], campo3[5:], modulo10(campo3))

        return "{0} {1} {2} {3} {4}".format(campo1, campo2, campo3, campo4, campo5)

    @property
    def codigo_barras_dv(self):
        return self.codigo_barras[4]

    @property
    def codigo_barras(self):
        cod_bar_fmt1 = "{banco}{moeda}"
        cod_bar_fmt2 = "{fator_vencto}{valor}{convenio}{conta_corrente}{num_sequencial}{carteira}"

        valor = str(int(self.valor_documento * Decimal(100.0)))

        cod_bar_part1 = cod_bar_fmt1.format(**{'banco':"{:0>3}".format(self._banco),
                                               'moeda':'9'})

        cod_bar_part2 = cod_bar_fmt2.format(**{'fator_vencto': "{:0>4}".format(self.fator_vencimento)[-4:],
                                               'valor': "{:0>10}".format(valor)[-10:],
                                               'convenio': "{:0>6}".format(self.convenio)[-6:],
                                               'conta_corrente': "{:0>8}".format(self.conta_corrente)[-8:],
                                               'num_sequencial': "{:0>9}".format(self.num_sequencial)[-9:],
                                               'carteira': "{:0>2}".format(self.carteira)[-2:]})

        dv = modulo11("{0}{1}".format(cod_bar_part1, cod_bar_part2))
        return "{0}{1}{2}".format(cod_bar_part1, dv, cod_bar_part2)

    def validate(self):
        super(CecredBoleto, self).validate()

        if not self.convenio or not isinstance(self.convenio, six.string_types):
            raise ValueError("convenio deve obrigatoriamente informado")
