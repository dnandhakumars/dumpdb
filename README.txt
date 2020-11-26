Mysqldump is a django package used to generate
the logical backup of the MySQL database.

Installation
    1. pip install mysqldump
    2. Add 'backupdb' to your 'settings.py'
    3. Run the below command
            ./manage.py dumpdb

setting.py
-------------- 

Installed apps

    INSTALLED_APPS = [
        'backupdb',
    ]

TMP_DIR

To define custom temporary dir, if not django will use default system tmp directory