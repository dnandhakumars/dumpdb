import os
import tempfile
from django.conf import settings

CUSTOM_MODULES = {
    'django.db.backends.mysql': 'dbmanager.dbbackends.mysql.MysqlDump',
}

# Custom Settings

# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB - 104857600
# 250MB - 214958080
# 500MB - 429916160

TMP_FILE_MAX_SIZE = getattr(settings, 'DBBACKUP_TMP_FILE_MAX_SIZE', 10485760)
TMP_FILE_READ_SIZE = getattr(settings, 'DBBACKUP_TMP_FILE_READ_SIZE', 1024 * 1000)

CONNECTORS = getattr(settings, 'DATABASES', {})
DATABASES = getattr(settings, 'DATABASES', list(settings.DATABASES.keys()))

PROJ_DIR = getattr(settings, 'BASE_DIR')

# define temporary directory or get default system tmp dir
TMP_DIR = getattr(settings, 'TMP_DIR', tempfile.gettempdir())

DUMP_DIR = getattr(settings, 'DUMP_DIR', str(PROJ_DIR))