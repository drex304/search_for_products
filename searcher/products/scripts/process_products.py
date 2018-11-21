import logging


from products.tasks import source_products, write_products
from products.models import Source


logger = logging.getLogger(__name__)

def run():
    source_products()
    write_products(filepath='/tmp/all_products.csv')
