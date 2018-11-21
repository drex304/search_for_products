import logging


from products.constants import COMPRESSION_NONE, COMPRESSION_GZ, COMPRESSION_ZIP
from products.tasks import uncompress


from products.models import Source


logger = logging.getLogger(__name__)

def run():
    filepath = '/tmp/products.csv.gz'
    sdest_filepath = uncompress(filepath=filepath, compression=COMPRESSION_GZ)

    filepath = '/tmp/products.json'
    sdest_filepath = uncompress(filepath=filepath, compression=COMPRESSION_NONE)

    filepath = '/tmp/products.xml.zip'
    sdest_filepath = uncompress(filepath=filepath, compression=COMPRESSION_ZIP)
