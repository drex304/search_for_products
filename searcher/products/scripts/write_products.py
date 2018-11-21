import logging


from products.tasks import write_products



logger = logging.getLogger(__name__)

def run():
    write_products()
