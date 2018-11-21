import logging


from products.tasks import source_products
from products.models import Source


logger = logging.getLogger(__name__)

def run():
    sources = Source.objects.all()
    source_products(sources)
