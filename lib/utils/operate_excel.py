# -*- coding:utf-8 -*-
import os
import xlrd
import xlwt


def read_excel(file: str) -> list:
    r"""Parse the table and compose the new data source.

    :param file: File path, str object.
    :return: The table is composed of data after parsing.
    :rtype: list object.

    """

    workbook = xlrd.open_workbook(file)
    table = workbook.sheet_by_index(0)
    rows, cols_name, list__ = table.nrows, table.row_values(0), []

    for row in range(1, rows):
        data = table.row_values(row)

        if data:
            content = {}
            for index in range(len(cols_name)):
                content[cols_name[index]] = data[index]
            list__.append(content)

    return list__


if __name__ == '__main__':
    pass
