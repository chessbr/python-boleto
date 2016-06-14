[![Build Status](https://travis-ci.org/rockho-team/python-boleto.svg?branch=master)](https://travis-ci.org/rockho-team/python-boleto)
[![Coverage Status](https://coveralls.io/repos/github/rockho-team/python-boleto/badge.svg?branch=master)](https://coveralls.io/github/rockho-team/python-boleto?branch=master)
[![License](https://img.shields.io/badge/license-AGPLv3-blue.svg)](LICENSE)

# Python Boleto
A Python library for generating Boletos. Boletos can be currently exported to
HTML.
[Jinja2](http://jinja.pocoo.org/) is used to render the boleto templates and
[JSBarcode](https://github.com/lindell/JsBarcode) is used to generate the bar
code inside a HTML canvas - so we don't need to render any image! Also, images
can be added in templates through Base64 encoding or through urls.

## Banks
Here are some implemented bank layouts. If your bank is not implemented yet, you could
help us: just fork our project and submit a pull request.

* [x] 085 - CECRED
* [ ] 001 - Banco do Brasil
* [ ] 104 - CEF
* [ ] 237 - Bradesco
* [ ] 341 - Itau
* [ ] 033 - Santander

## Compatibility
* [Tested on Python 2.7, 3.4 and 3.5](https://travis-ci.org/rockho-team/python-boleto)


## Usage

To use Python Boleto is easy, just import your bank module and instantiate its
class and export to HTML. Thanks to the [JSBarcode](https://github.com/lindell/JsBarcode) project,
we don't need to generate any image for barcode.

```python
from python_boleto.cecred import CecredBoleto

info = {'cedente':'Fulado Beltrano', } # popula com os dados do boleto

boleto = CecredBoleto(**info)
html = boleto.export_html()

print(html)
```

You can always implement your custom bank layout. All you need to do is subclass
`base.Boleto` class and override base methods, change template file name and
bank number.

Copyright
---------
Copyright (C) 2016 by [Rockho Team](https://github.com/rockho-team)


License
-------

Python Boleto is published under the GNU Affero General Public License,
version 3 (AGPLv3) (see the [LICENSE](LICENSE) file) and uses third party
libraries that are distributed under their own terms (see the [LICENSE-3RD-PARTY](LICENSE-3RD-PARTY) file).
