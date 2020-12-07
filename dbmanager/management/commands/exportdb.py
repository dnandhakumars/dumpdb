import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections
from ...dbbackends.base import get_module
from ...exceptions import ImproperEngine, DatabaseNotFoundException
from ...utilities import compress_file_gzip, get_db_keys

class Command(BaseCommand):
    """
    dumpdb command to dump data from current or mentioned database(s)
    """

    help = 'Dump and Restore Database'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--databases', nargs='+',
                            help="To dump selected db --databases [OPTIONS] DB1,DB2,DB3...]")
        parser.add_argument('-gz', '--compress', action='store_true',
                            help='to compress dump file')
        parser.add_argument('-itbl', '--ignore-table', nargs='+',
                            help="To ignore specified table(s) which must be specified using both the database and table names. eg: dbname.tbl_name")
        parser.add_argument('-tbl', '--tables', nargs='+',
                            help="To dump specified table(s) which must be specified after db name. eg: -d dbname -tbl tbl_name1, tbl_name2....")

    def handle(self, *args, **options):
        opt_databases   = options.get('databases', None)
        self.compress   = options.get('compress', False)

        db_keys = get_db_keys(opt_databases) or settings.DATABASES
        self.stdout.write(self.style.MIGRATE_HEADING('Running exportdb:'))
        if db_keys:
            for db_key in db_keys:
                conn = connections[db_key]
                engine = conn.settings_dict['ENGINE'].split('.')[-1]
                if engine == 'dummy':
                    raise ImproperEngine(conn.settings_dict['ENGINE'])
                else:
                    self.connector = get_module(db_key, conn)
                    database = self.connector.settings
                    self.connector.ignore_tabled = options.get('ignore_table') or []
                    self.connector.req_tables = options.get('tables') or []
                    self.dump_db(database)
        else:
            self.stdout.write(self.style.HTTP_INFO('No database(s) available to backup/restore.'))
    
    def dump_db(self, database):
        """
        Save a new backup file.
        """
        self.stdout.write(self.style.WARNING('Selected Database: '+ database.get('NAME')))
        filename = self.connector.get_filename(datetime.datetime.now())
        self.stdout.write(self.style.MIGRATE_LABEL('Processing file: '+ filename))
        outputfile = self.connector.create_db_dump()
        #compress file
        if self.compress:
            outputfile, filename = compress_file_gzip(filename, outputfile)
        self.connector.write_file_to_local(outputfile, filename)
        self.stdout.write(self.style.SUCCESS('Dump completed on '+ datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S") +'.'))
            