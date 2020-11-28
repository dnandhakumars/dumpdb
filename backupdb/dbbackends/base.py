import os
import shlex
import datetime
from django.core.files.base import File
from tempfile import SpooledTemporaryFile
from subprocess import Popen
from importlib import import_module
from backupdb import settings, exceptions
from shutil import copyfileobj

class BaseSettingsConverter(object):
    """
    Base class to get all db settings 
    """
    file_extension = 'dump'
    exclude = []

    def __init__(self, database_name=None, **kwargs):
        from django.db import connections, DEFAULT_DB_ALIAS
        self.database_name = (database_name or DEFAULT_DB_ALIAS)
        self.connection = connections[self.database_name]
        for attr, value in kwargs.items():
            setattr(self, attr.lower(), value)
    
    @property
    def settings(self):
        #add settings to selected module
        if not hasattr(self, '_settings'):
            sett = self.connection.settings_dict.copy()
            sett.update(settings.DATABASES.get(self.database_name, {}))
            self._settings = sett
        return self._settings

    def get_filename(self, curr_time):
        return "{timestamp}_{dbname}.{Extn}".format(timestamp = curr_time.strftime("%Y%m%d%H%M%S%f"), dbname = self.name, Extn=self.file_extension)

    def create_dump(self):
        dump = self._create_dump()
        return dump

    def write_file_to_local(self, outputfile, filename):
        custom_path = settings.DUMP_DIR
        if os.getcwd() == custom_path:
            dump_file = custom_path+'/'+filename
        else:
            stripped_path = custom_path.strip('/')
            try:
                os.makedirs(stripped_path, exist_ok=True)
            except OSError as e:
                raise exceptions.CustomFileException(e)
            dump_file = (stripped_path+'/'+filename)
        
        #seek(0), which means absolute file positioning
        outputfile.seek(0)
        with open(dump_file, 'wb') as fd:
            copyfileobj(outputfile, fd)
        
class CommonBaseCommand(BaseSettingsConverter):
    """
    To run import/export command.
    """

    def run_command(self, command, stdin=None, env=None):
        
        #commands as list
        cmd = shlex.split(command)

        # creating file obj
        stdout = SpooledTemporaryFile(max_size=settings.TMP_FILE_MAX_SIZE, dir=settings.TMP_DIR)
        stderr = SpooledTemporaryFile(max_size=settings.TMP_FILE_MAX_SIZE, dir=settings.TMP_DIR)

        try:
            if isinstance(stdin, File):
                process = Popen(cmd, stdin=stdin.open("rb"), stdout=stdout, stderr=stderr)
            else:
                process = Popen(cmd, stdin=stdin, stdout=stdout, stderr=stderr)
            process.wait()      #Wait for child process to terminate
            if process.poll():  #Check if child process has terminated
                raise exceptions.SubProcessException(process.stderr)
            return stdout, stderr
        except OSError as err:
            raise exceptions.ProcessException(err)

def get_module(database_name=None, conn=None):
    """
        Get required function as module based on db engine
    """
    engine = conn.settings_dict.get('ENGINE', None)
    conn_settings = conn.settings_dict
    connector_path = conn_settings.get('CONNECTOR', settings.CUSTOM_MODULES[engine])
    module_path = ('.'.join(connector_path.split('.')[:-1]))
    module_name = connector_path.split('.')[-1]
    module = import_module(module_path)
    connector = getattr(module, module_name)
    return connector(database_name, **conn_settings)