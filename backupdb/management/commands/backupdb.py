import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections
from ...dbbackends.base import get_module
from ...exceptions import ImproperEngine
from ...utilities import compress_file_gzip

class Command(BaseCommand):
    """
    dumpdb command to dump data from current or mentioned database(s)
    """

    help = 'Dump and Restore Database'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--databases', nargs='+', help="To dump selected db --databases [OPTIONS] DB1,DB2,DB3...]")
        parser.add_argument('-gz', '--compress', action='store_true', help='to compress dump file')

    def handle(self, *args, **options):
        opt_databases = options.get('databases', None)
        self.compress = options.get('compress', False)

        db_keys = self.get_db_keys(opt_databases) or settings.DATABASES
        if db_keys:
            for db_key in db_keys:
                conn = connections[db_key]
                engine = conn.settings_dict['ENGINE'].split('.')[-1]
                if engine == 'dummy':
                    raise ImproperEngine(conn.settings_dict['ENGINE'])
                else:
                    self.connector = get_module(db_key, conn)
                    database = self.connector.settings
                    self.dump_db(database)
        else:
            self.stdout.write(self.style.MIGRATE_HEADING('Running backupdb:'))
            self.stdout.write(self.style.HTTP_INFO('No database(s) available to backup/restore.'))
    
    def dump_db(self, database):
        """
        Save a new backup file.
        """
        self.stdout.write(self.style.MIGRATE_HEADING('Running backupdb:'))
        self.stdout.write(self.style.WARNING('Selected Database: '+ database.get('NAME')))
        print(datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S") )
        now = datetime.datetime.now()
        filename = self.connector.get_filename(now)
        outputfile = self.connector.create_dump()

        #compress file
        if self.compress:
            outputfile, filename = compress_file_gzip(filename, outputfile)
                    
        self.connector.write_file_to_local(outputfile, filename)

        self.stdout.write(self.style.MIGRATE_LABEL('Processing file: '+ filename))
        self.stdout.write(self.style.SUCCESS('Dump completed on '+ now.strftime("%Y-%b-%d %H:%M:%S") +''))
        print(datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S") )
        
    def get_db_keys(self, databases):
        """
        to get db key(s) using database name,
        if --database param used
        """
        if databases:
            db_keys = []
            for db_key, db_val in settings.DATABASES.items():
                if db_val['NAME'] in databases:
                    db_keys.append(db_key)
            return db_keys