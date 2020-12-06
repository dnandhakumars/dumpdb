class Error(Exception):
    """Base class for other exceptions"""
    pass

class ImproperEngine(Error):
    """Raised when the engine value is dummy"""

    def __init__(self, engine_val, message = "The DATABASES setting must configure a default database"):
        self.engine = engine_val
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.engine} -> {self.message}'

class CustomFileException(Error):
    """Raised when unable to create custom directory"""

    def __init__(self, error_obj, message = "Unable to create directory"):
        self.error_type = error_obj.strerror
        self.dir_path = error_obj.filename
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.error_type} -> {self.message} -> {self.dir_path}'

class CustomCommandException(Error):
    """Raised when subprocess.popen faced blocks"""

    def __init__(self, message = "Subprocess failed"):
        exclude_str = 'mysqldump: [Warning] Using a password on the command line interface can be insecure.'
        msg = message.replace(exclude_str, '')
        self.message = msg
        super().__init__(self.message)

    def __str__(self):
        return self.message

class DatabaseNotFoundException(Error):
    """Raised when database not found"""

    msg = {
        1049 : "Unknown database(s) {} when selecting the database(s)."
    }

    def __init__(self, err_code, dbname , message = "Command failed"):
        if err_code:
            self.message = self.msg.get(err_code).format(dbname)
        else:
            self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message