import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections, DEFAULT_DB_ALIAS
from ...dbconnect.base import get_module

class Command(BaseCommand):
    """
    dumpdb command to dump data from current or mentioned database(s)
    """

    help = 'Dump and Restore Database'


    def dump_db(self, database):
        """
        Save a new backup file.
        """
        self.stdout.write(self.style.WARNING('Selected Database: '+ database.get('NAME')))

        filename = self.connector.get_filename_path(database)
        outputfile = self.connector.create_dump()
        self.connector.write_local_file(outputfile, filename)
        now = datetime.datetime.now()

        self.stdout.write(self.style.MIGRATE_LABEL('Processing file: '+ filename))
        self.stdout.write(self.style.SUCCESS('Dump completed on '+ now.strftime("%Y-%b-%d %H:%M:%S") +''))

    def add_arguments(self, parser):
        #parser.add_argument('-d', '--database', action="store_true", help='')
        pass

    def handle(self, *args, **options):
        db_keys = settings.DATABASES
        for db_key in db_keys:
            database_key = db_key or DEFAULT_DB_ALIAS
            conn = connections[database_key]
            engine = conn.settings_dict['ENGINE'].split('.')[-1]
            if engine == 'dummy':
                pass
            else:
                self.connector = get_module(database_key, conn)
                database = self.connector.settings
                self.dump_db(database)