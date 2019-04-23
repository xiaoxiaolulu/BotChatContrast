# -*- coding:utf-8 -*-
import os
import six
import abc
import logging
from colorama import Fore, init
from lib.utils import time_setting
from logging.handlers import TimedRotatingFileHandler

init(autoreset=True)

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0


@six.add_metaclass(abc.ABCMeta)
class Color(object):

    @abc.abstractmethod
    def get_color_by_str(self, color_str):
        pass

    @abc.abstractmethod
    def get_all_colors(self):
        pass

    @abc.abstractmethod
    def get_color_set(self):
        pass


class ColorConfig(Color):

    FORE_GROUND_DEBUG = 'yellow'
    FORE_GROUND_INFO = 'green'
    FORE_GROUND_ERROR = 'red'
    FORE_GROUND_WARN = 'cyan'

    __COLOR = {
        'DEBUG': FORE_GROUND_DEBUG,
        'INFO': FORE_GROUND_INFO,
        'ERROR': FORE_GROUND_ERROR,
        'WARN': FORE_GROUND_WARN,
    }

    __COLORS = __COLOR.keys()
    __COLOR_SET = set(__COLOR)

    @classmethod
    def get_color_by_str(cls, color_str):
        if not isinstance(color_str, str):
            raise TypeError('the color type is not str {type}'.format(type=type(color_str)))
        color = str(color_str).upper()
        if color not in cls.__COLOR:
            raise KeyError('the color key {key} is not in color dic'.format(key=color))
        return cls.__COLOR[color]

    @classmethod
    def get_all_colors(cls):
        return cls.__COLORS

    @classmethod
    def get_color_set(cls):
        return cls.__COLOR_SET

    @classmethod
    def get_colors_dic(cls):
        return cls.__COLOR


class Logger(logging.Logger):

    def __init__(self, filemode='a', encoding='utf-8', level=DEBUG, stream=True, file=True):
        self.filename = os.path.join('./report/log/', '{}.log'.format(time_setting.timestamp()))
        self.mode = filemode
        self.encoding = encoding
        self.now = time_setting.timestamp('format_now')
        self.level = level
        super(Logger, self).__init__(self.now, level=level)
        self.file_handler = None
        if stream:
            self.set_stream_handler()
        if file:
            self.set_file_handler()

    def set_stream_handler(self, level=None):

        file_handler = TimedRotatingFileHandler(filename=self.filename, when='D', interval=1,
                                                backupCount=15, encoding=self.encoding)
        file_handler.suffix = '%Y-%m-%d-%H_%M_%S.log'
        if not level:
            file_handler.setLevel(self.level)
        else:
            file_handler.setLevel(level)
        formatter = logging.Formatter("[%(levelname)s] [%(asctime)s] %(filename)s [line:%(lineno)d] : %(message)s")

        file_handler.setFormatter(formatter)
        self.file_handler = file_handler
        self.addHandler(file_handler)

    def set_file_handler(self, level=None):
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(levelname)s] [%(asctime)s] %(filename)s [line:%(lineno)d] : %(message)s")
        stream_handler.setFormatter(formatter)
        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        self.addHandler(stream_handler)

    def reset_name(self, name):
        self.name = name
        self.removeHandler(self.file_handler)
        self.set_file_handler()


def coloring(msg, color="GREEN"):
    fore_color = getattr(Fore, color.upper())
    return fore_color + msg


def log_with_color(level, flag=False):

    def wrapper(msg):
        color = ColorConfig.get_colors_dic()[str(level).upper()]
        getattr(Logger(), level)(coloring(msg, color)) if flag else getattr(Logger(), level)(msg)

    return wrapper


log_info = log_with_color('info')
log_debug = log_with_color('debug')
log_warn = log_with_color('warn')
log_error = log_with_color('error')
