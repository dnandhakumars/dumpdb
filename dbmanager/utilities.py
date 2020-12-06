import gzip
import tempfile
from .settings import TMP_FILE_MAX_SIZE, TMP_DIR, TMP_FILE_READ_SIZE
from shutil import copyfileobj
from django.conf import settings
from .exceptions import DatabaseNotFoundException

def compress_file_gzip(filename, outputfile):
    """
    create a dest and copy file to dest
    using gzip compress the data.
    """
    temp_file = tempfile.SpooledTemporaryFile(max_size=TMP_FILE_MAX_SIZE, dir=TMP_DIR)
    fn = filename+".gz"
    outputfile.seek(0)
    with gzip.GzipFile(filename=fn, fileobj=temp_file, mode="wb") as fd:
        copyfileobj(outputfile, fd, TMP_FILE_READ_SIZE)
    return temp_file, fn

def decompress_file_gzip(inputfile):
    """
    create a dest and copy file to dest
    using gzip decompress the data.
    """
    temp_file = tempfile.SpooledTemporaryFile(max_size=TMP_FILE_MAX_SIZE, dir=TMP_DIR)
    inputfile.seek(0)
    read_zip = gzip.GzipFile(fileobj=inputfile, mode="rb")
    read_zip.seek(0)
    copyfileobj(read_zip, temp_file, TMP_FILE_READ_SIZE)
    return temp_file

def get_db_keys(databases):
    """
        To get db key(s) using database name,
        if --database param used
    """
    if databases:
        db_keys = []
        db_unknown = []
        for db_key, db_val in settings.DATABASES.items():
            if db_val['NAME'] in databases:
                db_keys.append(db_key)
            else:
                db_unknown.append(db_val['NAME'])
        if len(db_keys) > 0:
            return db_keys
        else:
            err_code = 1049
            raise DatabaseNotFoundException(err_code, db_unknown)