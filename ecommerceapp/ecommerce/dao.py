from django.db.models import Count

from .models import Product


def sreach_product(params={}):
    q = Product.objects.filter(active=True)

    kw = params.get('kw')
    if kw:
        q = q.filter(name__icontain=kw)

    prod_id = params.get('prod_id')
    if prod_id:
        q = q.filter(product_id=prod_id)

    return q