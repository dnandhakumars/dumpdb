Mysqldump is a django package used to generate the database backup(s) and to restore it.

## Installation
    * pip install mysqldump
    * Add 'dbmanager' to your 'settings.py'
    * Run the below command to backup all database(s) configured inside *settings.py*
        * ./manage.py backupdb

## setting.py
-----------------

** Installed apps: **

Add 'dbmanager' to your 'settings.py'

```
    INSTALLED_APPS = [
        'dbmanager',
    ]
```

** TMP_DIR **

By default package will use system tmp directory.

```
    TMP_DIR = '/var/www/html/my_project/tmp/'
```


** DUMP_DIR **

By default file will be stored in project container directory.
Specify the location to store the dumped file(s).

```
    DUMP_DIR = '/var/www/html/my_project/backup_dir/'
```



## Commands
------------

*backupdb* will dump all database(s) specified inside **settings.py**.

```
    ./manage.py backupdb

Running backupdb:
Selected Database: db_name1
Processing file: 20201130095543386091_db_name1.dump
Dump completed on 2020-Nov-30 09:55:43

```

To dump specified database using database name.

-d, --databases

```
    ./manage.py backupdb --databases db_name1 db_name2 ....

Running backupdb:
Selected Database: db_name1
Processing file: 20201130095543386091_db_name1.dump
Dump completed on 2020-Nov-30 09:55:43
Running backupdb:
Selected Database: db_name1
Processing file: 20201130095543920698_db_name2.dump
Dump completed on 2020-Nov-30 09:55:43

```

To archive the dump data with gzip.

-gz, --compress

```
    ./manage.py backupdb --compress

Running backupdb:
Selected Database: db_name1
Processing file: 20201130095543386091_db_name1.dump.gz
Dump completed on 2020-Nov-30 09:55:43

```

To dump specified table from database.

-tbl, --tables

```
    ./manage.py backupdb -d db_name1 --tables tbl_name1 tbl_name2
```

To ignore specified table from database(s).

-itbl, --ignore-table

```
    ./manage.py backupdb -d db_name1 --ignore-table db_name1.tbl_name1
```

multiple databases can be used while using *--ignore-table*.

```
    ./manage.py backupdb -d db_name1 db_name2 --ignore-table db_name1.tbl_name1 db_name2.tbl_name2

```