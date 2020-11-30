import gzip
import tempfile
from .settings import TMP_FILE_MAX_SIZE, TMP_DIR, TMP_FILE_READ_SIZE
from shutil import copyfileobj

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