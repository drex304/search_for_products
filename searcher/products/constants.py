
SOURCE_CSV = 1
SOURCE_JSON = 2
SOURCE_XML = 3


SOURCE_CHOICES = (
    (SOURCE_CSV, 'CSV'),
    (SOURCE_JSON, 'JSON'),
    (SOURCE_XML, 'XML'),
)


COMPRESSION_NONE = 1
COMPRESSION_GZ = 2
COMPRESSION_ZIP = 3


COMPESSION_CHOICES = (
    (COMPRESSION_NONE, 'None'),
    (COMPRESSION_GZ, 'GZ'),
    (COMPRESSION_ZIP, 'ZIP'),
)
