# This file is part of the sale_product_shop module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class SaleProductShopTestCase(ModuleTestCase):
    'Test Sale Product Shop module'
    module = 'sale_product_shop'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        SaleProductShopTestCase))
    return suite