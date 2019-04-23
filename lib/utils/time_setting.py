import time


def timestamp(format_key: str = 'format_now') -> str:
    r"""Format time

    :param format_key: You need to format the time, str object.
    :return: Formatted time.
    :rtype: str object.
    """

    format_time = {
        'default':
            {
                'format_day': '%Y-%m-%d',
                'format_now': '%Y-%m-%d-%H_%M_%S',
                'unix_now': '%Y-%m-%d %H:%M:%S',
            }
    }
    return time.strftime(format_time['default'][format_key], time.localtime(time.time()))
