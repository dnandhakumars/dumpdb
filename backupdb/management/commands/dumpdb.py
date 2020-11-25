from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections, DEFAULT_DB_ALIAS
from ...dbconnect.base import get_connector

class Command(BaseCommand):
    """
    dumpdb command to dump data from current or mentioned database(s)
    """

    def dump_db(self, database):
        """
        Save a new backup file.
        """
        self.stdout.write(self.style.WARNING('Selected Database: '+ database.get('NAME')))
        filename = self.connector.generate_filename(database)
        outputfile = self.connector.create_dump()
        outputfile.seek(0)
        self.stdout.write(self.style.MIGRATE_LABEL('Processing file: '+ filename))
        self.connector.write_local_file(outputfile, filename)
        self.stdout.write(self.style.SUCCESS('Successfully dumped data from "'+filename+'" database.'))

    def add_arguments(self,parser):
        #parser.add_argument('-d', '--database', action="store_true", help='to dump default primary database')
        pass

    def handle(self, *args, **options):
        db_keys = settings.DATABASES
        for db_key in db_keys:
            database_key = db_key or DEFAULT_DB_ALIAS
            conn = connections[database_key]
            self.connector = get_connector(database_key, conn)
            database = self.connector.settings
            self.dump_db(database)