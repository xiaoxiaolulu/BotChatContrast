# -*- coding:utf-8 -*-
import os
from lib.utils import time_setting as TS
from jinja2 import Environment, FileSystemLoader


PATH = os.path.abspath('./lib/templates')
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, )),
    trim_blocks=False)


def render_template(template_filename: str, content: dict):
    r"""Template rendering

    :param template_filename: Templates that need to be rendered, str object.
    :param content: Data to render, dict object.
    :return:
    """
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(content)


def create_test_report(name: str, header: dict, results: list) -> None:
    r"""Create test reports.

    :param name: The test report name, str object.
    :param header: Test each data header in the report, dict object.
    :param results: Values of test results, list object
    :return: None
    """
    name = "./report/report/{}_{}.html".format(name, TS.timestamp('format_day'))
    with open(name, 'w', encoding="utf-8") as f:
        html = render_template('index.html', {'header': header, "results": results})
        f.write(html)
        f.close()
