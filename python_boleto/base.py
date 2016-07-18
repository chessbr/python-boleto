# -*- coding: utf-8 -*-
# This file is part of Python Boleto.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

import base64
import datetime
from decimal import Decimal
import logging
import os

from jinja2 import Environment, PackageLoader
import six

from python_boleto import STATIC_DIR

from . import filters
from iso8601 import iso8601

if six.PY2:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class Boleto(object):
    '''
    Classe base que representa um boleto
    '''
    _template = 'generic.jinja'
    _banco = '000'
    _logo = ''

    # indica o numero unico do boleto, utilizado para
    # manter uma sequencia lógica
    num_sequencial = 0
    vencimento = None       # <datetime.datetime.date>
    data_documento = None   # <datetime.datetime.date>
    numero_documento = ''
    especie_documento = ''
    aceite = ''
    data_processamento = None   # <datetime.datetime.date>
    especie = ''
    quantidade = 0
    valor_unitario = Decimal()
    valor_documento = Decimal()
    instrucoes = []
    valor_desconto = Decimal()
    valor_outras_deducoes = Decimal()
    valor_multa = Decimal()
    valor_outros_acrescimos = Decimal()
    valor_cobrado = Decimal()
    sacado = ''
    sacado_extra = []
    cpf_cei_cnpj = ''
    sacador_avalista = ''
    local_pagamento = ''
    cedente = ''
    agencia = ''
    conta_corrente = ''
    carteira = ''
    contrato = ''
    informacoes = []

    def __init__(self, **kwargs):
        '''
        Inicializa os atributos, se os informados em `kwargs` existirem
        '''

        for k, v in kwargs.items():
            # as propriedades banco e template não podem ser alteradas no init
            if not k in ('banco', 'template') and hasattr(self, k):
                setattr(self, k, v)

    def __setattr__(self, name, value):
        '''
        Transforma os valores de acordo com os tipos
        '''
        if name in ('valor_unitario', 'valor_documento', 'valor_desconto',
                    'valor_outras_deducoes', 'valor_multa', 'valor_outros_acrescimos',
                    'valor_cobrado'):
            value = Decimal(value)

        elif name in ('vencimento', 'data_documento', 'data_processamento'):
            if isinstance(value, six.string_types):
                value = iso8601.parse_date(value).date()

        elif name in ('quantidade', 'num_sequencial'):
            try:
                value = int(value)
            except:
                value = 0
                
        elif name in ('numero_documento', 'especie_documento', 'aceite', 'especie', 'sacado',
                      'cpf_cei_cnpj', 'sacador_avalista', 'local_pagamento', 
                      'cedente', 'agencia', 'conta_corrente', 'carteira', 'contrato'):
            value = "{0}".format(value)

        return super(Boleto, self).__setattr__(name, value)

    @property
    def nosso_numero(self):
        ''' Calcula e retorna o nosso número '''
        raise NotImplementedError()

    @property
    def linha_digitavel(self):
        ''' Calcula e retorna a linha digitáveli do boleto '''
        raise NotImplementedError()

    @property
    def codigo_barras_dv(self):
        ''' Calcula e retorna o DV do código de barras '''
        raise NotImplementedError()

    @property
    def codigo_barras(self):
        ''' Calcula e retorna o código de barras do boleto '''
        raise NotImplementedError()

    def export_html(self, include_recibo_sacado=True, static_url=None):
        ''' Gera e retorna o boleto em HTML '''
        env = Environment(loader=PackageLoader('python_boleto', 'templates'))
        env.filters['index_or_blank'] = filters.index_or_blank
        env.filters['format_currency_or_blank'] = filters.format_currency_or_blank
        env.filters['format_date_or_blank'] = filters.format_date_or_blank
        env.filters['format_agencia_conta'] = filters.format_agencia_conta
        template = env.get_template(self._template)

        context_data = self.get_context_data() or {}

        # Monta a URL do logo do banco
        logo_url = self._logo
        if static_url:
            logo_url = urljoin(static_url, self._logo)
        context_data['logo_url'] = logo_url

        # gera o barse64 do logo, se possível
        try:
            logo_img_file = os.path.join(STATIC_DIR, self._logo)
            if os.path.exists(logo_img_file):
                img = open(logo_img_file, "rb")
                context_data['logo_base64'] = base64.b64encode(img.read()).decode('utf-8')
        except:
            logger.exception("Erro ao converter logo em Base64")

        return template.render(boleto=self,
                               include_recibo_sacado=include_recibo_sacado,
                               **context_data)

    def validate(self):
        '''
        Valida os dados do boleto, lançando excessões o erro.
        '''

        # inteiros
        if not isinstance(self.num_sequencial, six.integer_types):
            raise TypeError("num_sequencial deve ser um inteiro")
        elif self.num_sequencial <= 0:
            raise ValueError("num_sequencial deve maior que zero")

        elif not isinstance(self.quantidade, six.integer_types):
            raise TypeError("quantidade deve ser um inteiro")
        elif self.quantidade < 0:
            raise ValueError("quantidade deve maior ou igual a zero")

        # datas
        elif not isinstance(self.vencimento, datetime.date):
            raise TypeError("vencimento deve ser do tipo data")

        elif not self.data_documento is None and not isinstance(self.data_documento, datetime.date):
            raise TypeError("data_documento deve ser do tipo data")

        elif not self.data_processamento is None and not isinstance(self.data_processamento, datetime.date):
            raise TypeError("data_processamento deve ser do tipo data")


        # decimais
        elif not isinstance(self.valor_unitario, Decimal):
            raise TypeError("valor_unitario deve ser do tipo Decimal")

        elif not isinstance(self.valor_documento, Decimal):
            raise TypeError("valor_documento deve ser do tipo Decimal")

        elif not isinstance(self.valor_desconto, Decimal):
            raise TypeError("valor_desconto deve ser do tipo Decimal")

        elif not isinstance(self.valor_outras_deducoes, Decimal):
            raise TypeError("valor_outras_deducoes deve ser do tipo Decimal")

        elif not isinstance(self.valor_multa, Decimal):
            raise TypeError("valor_multa deve ser do tipo Decimal")

        elif not isinstance(self.valor_outros_acrescimos, Decimal):
            raise TypeError("valor_outros_acrescimos deve ser do tipo Decimal")

        elif not isinstance(self.valor_cobrado, Decimal):
            raise TypeError("valor_cobrado deve ser do tipo Decimal")

        # strings
        elif not isinstance(self.numero_documento, six.string_types):
            raise TypeError("numero_documento deve ser uma string")

        elif not isinstance(self.especie_documento, six.string_types):
            raise TypeError("especie_documento deve ser uma string")

        elif not isinstance(self.aceite, six.string_types):
            raise TypeError("aceite deve ser uma string")

        elif not isinstance(self.especie, six.string_types):
            raise TypeError("especie deve ser uma string")

        elif not isinstance(self.sacado, six.string_types):
            raise TypeError("sacado deve ser uma string")

        elif not isinstance(self.cpf_cei_cnpj, six.string_types):
            raise TypeError("cpf_cei_cnpj deve ser uma string")

        elif not isinstance(self.sacador_avalista, six.string_types):
            raise TypeError("sacador_avalista deve ser uma string")

        elif not isinstance(self.local_pagamento, six.string_types):
            raise TypeError("local_pagamento deve ser uma string")

        elif not isinstance(self.cedente, six.string_types):
            raise TypeError("cedente deve ser uma string")

        elif not isinstance(self.agencia, six.string_types):
            raise TypeError("agencia deve ser uma string")

        elif not isinstance(self.conta_corrente, six.string_types):
            raise TypeError("conta_corrente deve ser uma string")

        elif not isinstance(self.carteira, six.string_types):
            raise TypeError("carteira deve ser uma string")

        elif not isinstance(self.contrato, six.string_types):
            raise TypeError("contrato deve ser uma string")

        # listas
        elif self.instrucoes and not isinstance(self.instrucoes, list):
            raise TypeError("instrucoes deve ser do tipo list")

        elif self.informacoes and not isinstance(self.informacoes, list):
            raise TypeError("informacoes deve ser do tipo list")

        elif self.sacado_extra and not isinstance(self.sacado_extra, list):
            raise TypeError("sacado_extra deve ser do tipo list")


    def get_context_data(self):
        '''
        Obtém informações adicionais do boleto para serem utilizadas
        no render do boleto HTML ou em qualquer outra ocasião
        :rtype: dict|None
        '''
        pass
