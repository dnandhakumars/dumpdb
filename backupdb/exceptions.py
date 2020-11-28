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

class SubProcessException(Error):
    """Raised when subprocess faced blocks"""

    def __init__(self, error_obj, message = "Subprocess failed"):
        self.error_type = error_obj.read()
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.error_type} -> {self.message}'

class SubProcessException(Error):
    """Raised when main process faced blocks"""
    def __init__(self, error_obj, message = "Process failed"):
        self.error_type = error_obj
        self.message = message
        super().__init__(self.message)