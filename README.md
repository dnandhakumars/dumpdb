Mysqldump is a django package to import and export mysql database.

## Installation
    * pip install mysqldump
    * Add 'dbmanager' to your 'settings.py'
    * Run the below command to backup all database(s) configured inside *settings.py*
        ```
            $ ./manage.py exportdb
        ```

## setting.py
-----------------

**Installed apps:**

Add 'dbmanager' to your 'settings.py'

```
    INSTALLED_APPS = [
        'dbmanager',
    ]
```

**TMP_DIR**

Package will use system default tmp directory, if not specified.

```
    TMP_DIR = '/var/www/html/my_project/tmp/'
```


**DUMP_DIR**

By default dump file(s) will be stored in project container directory.
Specify the location to store the dumped file(s).

```
    DUMP_DIR = '/var/www/html/my_project/backup_dir/'
```



## Commands
------------

## Export Database ##

**exportdb** will dump all database(s) specified inside **settings.py**.

```
    $ ./manage.py exportdb

Running exportdb:
Selected Database: db_name1
Processing file: 20201130095543386091_db_name1.dump
Dump completed on 2020-Nov-30 09:55:43

```

- To dump specified database using database name.

    -d, --databases

```
    $ ./manage.py exportdb --databases db_name1 db_name2 ....

Running exportdb:
Selected Database: db_name1
Processing file: 20201130095543386091_db_name1.dump
Dump completed on 2020-Nov-30 09:55:43
Running exportdb:
Selected Database: db_name1
Processing file: 20201130095543920698_db_name2.dump
Dump completed on 2020-Nov-30 09:55:43

```

- To archive the dump data with gzip.

    -gz, --compress

```
    $ ./manage.py exportdb --compress

Running exportdb:
Selected Database: db_name1
Processing file: 20201130095543386091_db_name1.dump.gz
Dump completed on 2020-Nov-30 09:55:43

```

- To dump specified table from database.

    -tbl, --tables

```
    $ ./manage.py exportdb -d db_name1 --tables tbl_name1 tbl_name2
```

- To ignore specified table from database(s).

    itbl, --ignore-table

```
    $ ./manage.py exportdb -d db_name1 --ignore-table db_name1.tbl_name1
```

```
    $ ./manage.py exportdb -d db_name1 db_name2 --ignore-table db_name1.tbl_name1 db_name2.tbl_name2

```

## Import Database ##

**importdb** to restore the specified database.

- By default package will check project container directory or DUMP_DIR for the file.

    -f, --filename

```
    $ ./manage.py importdb dbname1 -f db_name1.dump.gz

Running importdb:
Selected Database: db_name1
Processing file: db_name1.dump.gz
Restore completed on 2020-Nov-30 09:55:43

```