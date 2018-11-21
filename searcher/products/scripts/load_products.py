import logging


from products.constants import SOURCE_CSV, SOURCE_JSON, SOURCE_XML
from products.tasks import load_products


from products.models import Source, Product


logger = logging.getLogger(__name__)

def run():
    products = Product.objects.all()
    logger.info("cleaning up {} old products...".format(len(products)))
    products.delete()
    # filepath = '/tmp/products.csv'
    # sdest_filepath = load_products(filepath=filepath, format=SOURCE_CSV)

    # filepath = '/tmp/products.json'
    # sdest_filepath = load_products(filepath=filepath, format=SOURCE_JSON)
    #
    filepath = '/tmp/products.xml'
    sdest_filepath = load_products(filepath=filepath, format=SOURCE_XML)
