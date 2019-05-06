# -*- coding: utf-8 -*-
import re


def custom_manage(custom: str, relevance: dict) -> str:
    r""" Relevance test interface

    :param custom: Data sources that need to be defined, str object.
    :param relevance: Associated fields, dict object.
    :return: The completed data has been defined
    :rtype: str object.
    """
    if isinstance(custom, str):
        try:
            relevance_list = re.findall("\${(.*?)}\$", custom)
            for n in relevance_list:
                pattern = re.compile('\${' + n + '}\$')
                custom = re.sub(pattern, relevance[n], custom, count=1)
        except TypeError:
            pass
        return custom


if __name__ == "__main__":
    pass