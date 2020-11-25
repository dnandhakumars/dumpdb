import os
import shlex
from django.core.files.base import File
from tempfile import SpooledTemporaryFile
from subprocess import Popen
from importlib import import_module
from backupdb import settings
from shutil import copyfileobj

CONNECTOR_MAPPING = {
    'django.db.backends.sqlite3': 'backupdb.dbconnect.sqlite.SqliteConnector',
    'django.db.backends.mysql': 'backupdb.dbconnect.mysql.MysqlDumpConnector',
    'django.db.backends.postgresql': 'backupdb.dbconnect.postgresql.PgDumpConnector',
    'django.db.backends.postgresql_psycopg2': 'backupdb.dbconnect.postgresql.PgDumpConnector',
    'django.db.backends.oracle': None,
    'django_mongodb_engine': 'backupdb.dbconnect.mongodb.MongoDumpConnector',
    'djongo': 'backupdb.dbconnect.mongodb.MongoDumpConnector',
    'django.contrib.gis.db.backends.postgis': 'backupdb.dbconnect.postgresql.PgDumpGisConnector',
    'django.contrib.gis.db.backends.mysql': 'backupdb.dbconnect.mysql.MysqlDumpConnector',
    'django.contrib.gis.db.backends.oracle': None,
    'django.contrib.gis.db.backends.spatialite': 'backupdb.dbconnect.sqlite.SqliteConnector',
}



def get_connector(database_name=None, conn=None):
    """
    Get a connector from its database key in setttings.
    """
    engine = conn.settings_dict['ENGINE']
    connector_settings = settings.CONNECTORS.get(database_name, {})
    connector_path = connector_settings.get('CONNECTOR', CONNECTOR_MAPPING[engine])
    dumper_module_path = ('.'.join(connector_path.split('.')[:-1]))
    dumper_module_name = connector_path.split('.')[-1]
    module = import_module(dumper_module_path)
    
    connector = getattr(module, dumper_module_name)
    return connector(database_name, **connector_settings)

class BaseDBConnector(object):
    """
    Base class for create database connector. This kind of object creates
    interaction with database and allow backup and restore operations.
    """
    extension = 'dump'
    exclude = []

    def __init__(self, database_name=None, **kwargs):
        from django.db import connections, DEFAULT_DB_ALIAS
        self.database_name = (database_name or DEFAULT_DB_ALIAS)
        self.connection = connections[self.database_name]
        for attr, value in kwargs.items():
            setattr(self, attr.lower(), value)
    
    @property
    def settings(self):
        """Mix of database and connector settings."""
        if not hasattr(self, '_settings'):
            sett = self.connection.settings_dict.copy()
            sett.update(settings.DATABASES.get(self.database_name, {}))
            self._settings = sett
        return self._settings

    def generate_filename(self, database=None):
        return self.name+'.'+self.extension

    def create_dump(self):
        dump = self._create_dump()
        return dump

    def write_local_file(self, outputfile, filename):
        dump_file = filename
        outputfile.seek(0)
        with open(dump_file, 'wb') as fd:
            copyfileobj(outputfile, fd)
        
class BaseCommandDBConnector(BaseDBConnector):
    """
    Base class for create database connector based on command line tools.
    """
    dump_prefix = ''
    dump_suffix = ''
    restore_prefix = ''
    restore_suffix = ''

    use_parent_env = True
    env = {}
    dump_env = {}
    restore_env = {}

    def run_command(self, command, stdin=None, env=None):
        """
        Launch a shell command line.

        :param command: Command line to launch
        :type command: str
        :param stdin: Standard input of command
        :type stdin: file
        :param env: Environment variable used in command
        :type env: dict
        :return: Standard output of command
        :rtype: file
        """
        cmd = shlex.split(command)
        stdout = SpooledTemporaryFile(max_size=settings.TMP_FILE_MAX_SIZE,
                                      dir=settings.TMP_DIR)
        stderr = SpooledTemporaryFile(max_size=settings.TMP_FILE_MAX_SIZE,
                                      dir=settings.TMP_DIR)
        full_env = os.environ.copy() if self.use_parent_env else {}
        full_env.update(self.env)
        full_env.update(env or {})
        try:
            if isinstance(stdin, File):
                process = Popen(
                    cmd, stdin=stdin.open("rb"), stdout=stdout, stderr=stderr,
                    env=full_env
                )
            else:
                process = Popen(cmd, stdin=stdin, stdout=stdout, stderr=stderr, env=full_env)
            process.wait()
            if process.poll():
                stderr.seek(0)
                self.stdout.write("Error running:")
            stdout.seek(0)
            stderr.seek(0)
            return stdout, stderr
        except OSError as err:
            self.stdout.write("Error running 1")
