import pathlib
import datetime
from django.core.management.base import BaseCommand
from django.db import connections
from ...utilities import get_db_keys
from ...exceptions import ImproperEngine
from ...dbbackends.base import get_module

class Command(BaseCommand):
    """
    To restore data to mentioned database
    """

    def add_arguments(self, parser):
        parser.add_argument('database', type=str,
                            help='provide database name to restore.')
        parser.add_argument('-f', '--filename',
                            help='Get file from "DUMP_DIR" by providing filename.')
        # parser.add_argument('-F', '--input-file',
        #                     help='Manual file path for restore file, e.g. "/home/mypc/downloads/restore_file.dump".')

    def handle(self, *args, **options):
        database = options.get('database',None)
        self.filename = options.get('filename', None)
        # self.input_path = options.get('input_file', None)
        db_keys = get_db_keys(database)
        self.stdout.write(self.style.MIGRATE_HEADING('Running importdb:'))
        if self.filename:
            if db_keys:
                for db_key in db_keys:
                    conn = connections[db_key]
                    engine = conn.settings_dict['ENGINE'].split('.')[-1]
                    if engine == 'dummy':
                        raise ImproperEngine(conn.settings_dict['ENGINE'])
                    else:
                        self.connector = get_module(db_key, conn)
                        curr_db = self.connector.settings
                        self.restoredb(curr_db)
            else:
                self.stdout.write(self.style.HTTP_INFO('No database(s) available to backup/restore.'))
        else:
            self.stdout.write(self.style.ERROR('Restore file not mentioned, use "-f" or "-F" for file selection.'))

    def restoredb(self, database):
        """
            to restore dump data to database
        """
        self.stdout.write(self.style.WARNING('Selected Database: '+ database.get('NAME')))
        dump_file, dump_filename = self.connector.get_dump_file(self.filename)
        self.stdout.write(self.style.MIGRATE_LABEL('Processing file: '+ dump_filename))
        dump_file.seek(0)
        result = self.connector.restore_db_dump(dump_file)
        dump_file.close()
        self.stdout.write(self.style.SUCCESS('Restore completed on '+ datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S") +'.'))
