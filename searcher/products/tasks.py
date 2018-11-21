import os
import wget
import gzip
import zipfile
import csv
import json
import logging
import xmltodict
import traceback


from products.constants import COMPRESSION_NONE, COMPRESSION_GZ, COMPRESSION_ZIP, \
    SOURCE_CSV, SOURCE_JSON, SOURCE_XML
from products.models import Source, Product


logger = logging.getLogger(__name__)



def source_products(source=None, output_path='/tmp'):
    """
    Using our sources, we fetch the product files, store them locally
    and process them.
    """
    logger.info("processing sources...")
    filepaths = []
    if source:
        sources = [source]
    else:
        sources = Source.objects.all()

    for s in sources:
        logger.info("processing source: {} .....".format(s))
        try:
            filename = wget.download(s.url, output_path)
            logger.info("source: {},  filename:  {}".format(s.url, filename))
            filepath = os.path.join(output_path, filename)
            process_files(filepath=filepath, compression=s.compression, format=s.format)
        except Exception as e:
            logger.error("Failed to download {} with {}, traceback: {}".format(source, e, traceback.format_exc()))



def process_files(filepath, compression=COMPRESSION_NONE, format=SOURCE_CSV):
    dest_filepath = uncompress(filepath=filepath, compression=compression)
    data = load_products(dest_filepath, format=format)


def uncompress(filepath, compression):
    """
    Hanles any uncression required based of the compression type.
    """
    logger.info("Uncompressing {} with ({})".format(filepath, compression))
    if compression == COMPRESSION_NONE:
        dest_filepath = filepath

    elif compression == COMPRESSION_GZ:
        dest_filepath = filepath.strip('.gz')
        with open(dest_filepath, 'wb') as df:
            with gzip.open(filepath ,'rb') as sf:
                df.write(sf.read())

    elif compression == COMPRESSION_ZIP:
        dest_filepath = filepath.strip('.zip')
        dir_name = os.path.dirname(dest_filepath)
        # assuming we only have one file in the zip file
        with zipfile.ZipFile(filepath, 'r') as sf:
            sf.extractall(dir_name)

    logger.info("filename after decompression: {}".format(dest_filepath))
    return dest_filepath


def is_true(value):
    """
    Helper function to deal with many affirmations
    """
    if str(value) in ['True', 'true', '1', 't', 'T' 'y', 'yes', 'Yes']:
        return True
    else:
        return False


def clean_price(value):
    """
    Helper function to deal with '' price values.
    """
    if value == '' or value is None:
        value = '0'
    return value

def clean_brand(value):
    """
    Helper function to deal with '' price values.
    """
    if value is None:
        value = ''
    return value


def update_product(entries):
        try:
            product = Product.objects.get(ext_id=entries['ext_id'], name=entries['name'])
        except Product.DoesNotExist:
            product = Product(ext_id=entries['ext_id'], name=entries['name'])
        product.brand = entries['brand']
        product.retailer = entries['retailer']
        product.price = entries['price']
        product.in_stock = entries['in_stock']
        product.source = entries['source']
        product.save()


def load_products(filepath, format):
    if format == SOURCE_CSV:
        load_csv_products(filepath=filepath, format=format)
    elif format == SOURCE_JSON:
        load_json_products(filepath=filepath, format=format)
    elif format == SOURCE_XML:
        load_xml_products(filepath=filepath, format=format)


def load_csv_products(filepath, format, output_on=5000):
    logger.info("Loading csv filepath {}".format(filepath))
    first = True
    counter = 0
    with open(filepath, 'r') as sf:
        lines = csv.reader(sf, delimiter=',', skipinitialspace=True, quotechar='"')
        # headers Id, Name, Brand, Retailer, Price, InStock
        for line in lines:
            try:
                if first:
                    first = False
                    continue
                data = {}
                data['ext_id'] = line[0]
                data['name'] = line[1]
                data['brand'] = line[2]
                data['retailer'] = line[3]
                data['price'] = clean_price(value=line[4])
                data['in_stock'] = is_true(line[5])
                data['source'] = format
                update_product(data)
                counter += 1
                if counter % output_on == 0:
                    logger.info('processed {} entries...'.format(counter))
            except Exception as e:
                logger.error("Failed to parse file {} with entry: {}, exception: {}".format(filepath, entry, e))



def load_json_products(filepath, format, output_on=5000):
    """
    data as:    "id": "02cd22d2e02b4a7086641ab9df01b",
                "name": "superplausible",
                "brand": "typothere",
                "retailer": "caffiso",
                "price": "",
                "in_stock": "n"
    """
    logger.info("Loading json filepath {}".format(filepath))
    counter = 0
    with open(filepath) as jf:
        json_data = json.load(jf)
        for entry in json_data:
            try:
                data = {}
                data['ext_id'] = entry['id']
                if 'name' in entry:
                    data['name'] = entry['name']
                else:
                    data['name'] = ''
                if 'brand' in entry:
                    data['brand'] = clean_brand(entry['brand'])
                else:
                    data['brand'] = ''
                if 'retailer' in entry:
                    data['retailer'] = entry['retailer']
                else:
                    data['retailer'] = ''
                if 'price' in entry:
                    data['price'] = clean_price(value=entry['price'])
                else:
                    data['price'] = '0'

                if 'in_stock' in entry:
                    data['in_stock'] = is_true(entry['in_stock'])
                else:
                    data['in_stock'] = False # assume that its not available
                data['source'] = format
                update_product(data)
                counter += 1
                if counter % output_on == 0:
                    logger.info('processed {} entries...'.format(counter))
            except Exception as e:
                logger.error("Failed to parse file {} with entry: {}, exception: {}".format(filepath, entry, e))
                raise


def load_xml_products(filepath, format, output_on=5000):
    """
    <?xml version="1.0" encoding="UTF-8" ?>
        <root>
            <item type="dict">
                <id type="str">271f5cf6c8484b30b66a0df1939e4</id>
                <name type="str">conventionalization</name>
                <brand type="str">geosynclinal</brand>
                <retailer type="str">jibstay</retailer>
                <latest_price type="str">310.82</latest_price>
                <available type="str">n</available>
            </item>
        </root>
    </xml>
    """
    logger.info("Loading xml filepath {}".format(filepath))
    data = {}
    counter = 0
    with open(filepath, 'rb') as fp:
        xml_data = xmltodict.parse(fp.read())
        for entry in xml_data['root']['item']:
            try:
                data['ext_id'] = entry['id']['#text']
                data['name'] = entry['name']['#text']
                if '#text' in entry['brand']:
                    data['brand'] = entry['brand']['#text']
                else:
                    data['brand'] = ''

                if '#text' in entry['retailer']:
                    data['retailer'] = entry['retailer']['#text']
                else:
                    data['retailer'] = ''
                data['price'] = clean_price(value=entry['latest_price']['#text'])
                data['in_stock'] = is_true(entry['available']['#text'])
                data['source'] = format
                update_product(data)
                counter += 1
                if counter % output_on == 0:
                    logger.info('processed {} entries...'.format(counter))

            except Exception as e:
                logger.error("Failed to parse file {} with entry: {}, exception: {}".format(filepath, entry, e))
                raise


def write_products(filepath='/tmp/all_products.csv'):
    headers = ['id', 'name', 'brand', 'retailer', 'price', 'in_stock', 'source']
    with open(filepath, 'w') as fp:
        csv_writer = csv.writer(fp, delimiter=',',
            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(headers)
        for product in Product.objects.all():
            csv_writer.writerow([product.ext_id, product.name, product.brand,
                product.retailer, product.price, product.in_stock,
                product.get_source_display()])
