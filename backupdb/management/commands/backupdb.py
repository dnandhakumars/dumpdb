import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections
from ...dbbackends.base import get_module
from ...exceptions import ImproperEngine

class Command(BaseCommand):
    """
    dumpdb command to dump data from current or mentioned database(s)
    """

    help = 'Dump and Restore Database'

    def dump_db(self, database):
        """
        Save a new backup file.
        """
        self.stdout.write(self.style.MIGRATE_HEADING('Running backupdb:'))
        self.stdout.write(self.style.WARNING('Selected Database: '+ database.get('NAME')))
        now = datetime.datetime.now()
        filename = self.connector.get_filename(now)
        outputfile = self.connector.create_dump()
        self.connector.write_file_to_local(outputfile, filename)

        self.stdout.write(self.style.MIGRATE_LABEL('Processing file: '+ filename))
        self.stdout.write(self.style.SUCCESS('Dump completed on '+ now.strftime("%Y-%b-%d %H:%M:%S") +''))

    def add_arguments(self, parser):
        #parser.add_argument('-d', '--database', action="store_true", help='')
        pass

    def handle(self, *args, **options):
        db_keys = settings.DATABASES
        if db_keys:
            for db_key in db_keys:
                database_key = db_key
                conn = connections[database_key]
                engine = conn.settings_dict['ENGINE'].split('.')[-1]
                if engine == 'dummy':
                    raise ImproperEngine(conn.settings_dict['ENGINE'])
                else:
                    self.connector = get_module(database_key, conn)
                    database = self.connector.settings
                    self.dump_db(database)
        else:
            self.stdout.write(self.style.MIGRATE_HEADING('Running backupdb:'))
            self.stdout.write(self.style.HTTP_INFO('No database(s) available to backup/restore.'))
        