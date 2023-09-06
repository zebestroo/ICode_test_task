import datetime
import logging


class Contract():
    __name = 'Untitled'
    __status = 'Draft'
    __project = 'Untitled'

    def __init__(self):
        self.__date = datetime.datetime.now()

    def confirm(self):
        self.__status = 'Active'

    def complete(self):
        self.__status = 'Completed'
        self.__date_of_signing = datetime.datetime.now()

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_status(self):
        return self.__status

    def get_project(self):
        return self.__project

    def set_project(self, project):
        self.__project = project

    def get_create_date(self):
        return self.__date

    def get_sign_date(self):
        return self.__date_of_signing

    def dump(self, cursor):
        cursor.execute(
            f"""INSERT INTO Contracts (name, create_date, status, project) VALUES ('{self.get_name()}', '{self.get_create_date().strftime('%Y-%m-%d %H:%M:%S')}', '{self.get_status()}', '{self.get_project()}')""")


class Project():
    __name = 'Untitled'

    def __init__(self):
        self.__date = datetime.datetime.now()

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_create_date(self):
        return self.__date

    def dump(self, cursor):
        cursor.execute(
            f"""INSERT INTO Projects (name, create_date) VALUES ('{self.get_name()}', '{self.get_create_date().strftime('%Y-%m-%d %H:%M:%S')}')""")


class CustomFormatter(logging.Formatter):

    grey = '\x1b[38;21m'
    green = '\x1b[32m'
    yellow = '\x1b[33m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.green + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
