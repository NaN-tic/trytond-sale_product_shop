# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['Sale']
__metaclass__ = PoolMeta


class Sale:
    __name__ = 'sale.sale'

    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()
        cls._error_messages.update({
                'not_available_in_shop': 'Product %s is not available for '
                    'its sale in shop %s.',
                })

    @classmethod
    def quote(cls, sales):
        cls.available_in_shop(sales)
        super(Sale, cls).quote(sales)

    @classmethod
    def check_product_shop(cls):
        if Transaction().context.get('without_warning'):
            return False
        return True

    @classmethod
    def available_in_shop(cls, sales):
        ProductShop = Pool().get('product.template-sale.shop')

        if not cls.check_product_shop():
            return

        for sale in sales:
            templates = list({l.product.template for s in sales
                for l in s.lines if l.product})
            shop_products = ProductShop.search([('template', 'in', templates)])
            products = [p for sp in shop_products
                for p in sp.template.products]
            for line in sale.lines:
                if (line.type == 'line' and line.product
                        and line.product not in products):
                    cls.raise_user_warning(
                        'not_available_in_shop_%s' % line.id,
                        'not_available_in_shop',
                        (line.product.name, sale.shop.name)
                        )
