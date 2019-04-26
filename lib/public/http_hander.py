# -*- coding:utf-8 -*-
from urllib import parse
import requests
import urllib3
import yaml
from lib.public import logger
from lib.public import relevance
from lib.utils.get_json_params import GetJsonParams

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BaseKeyWords(GetJsonParams):

    def __init__(self, request_file='./data/ChantBotApi.yaml'):
        self.request_file = request_file

    @staticmethod
    def post(**kwargs: dict) -> requests.Response:
        r"""Sends a POST request.

        :param kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return requests.post(verify=False, **kwargs)

    @staticmethod
    def get(**kwargs: dict) -> requests.Response:
        r"""Sends a GET request.

        :param kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return requests.get(**kwargs, verify=False)

    def make_test_templates(self, question: dict):
        r"""Run the test request case.

        :param question:   The robot test problem, dict object.
        :return: request.Response dict object
        :rtype: request.Response
        """

        try:
            body, out_values = {}, ''
            with open(self.request_file, 'r', encoding='utf-8') as file:
                items = yaml.load(file, Loader=yaml.FullLoader)
                for key, value in items.items():
                    if key == 'body':
                        relevance_body = relevance.custom_manage(str(items['body']), question)
                        body.update(eval(relevance_body))
                    else:
                        out_values += str(items['outValues'])

            method = GetJsonParams.get_value(body, 'method')
            if method in ['get', 'GET']:
                temp = ('url', 'params', 'headers')
                request_body = GetJsonParams.for_keys_to_dict(*temp, my_dict=body)
                if request_body['params']:
                    if '=' in request_body.get('params') or '&' in request_body.get('params'):
                        request_body['params'] = dict(parse.parse_qsl(request_body['params']))

                return self.get(**request_body).json(), out_values

            if method in ['post', 'POST']:
                temp = ('url', 'headers', 'json', 'data', 'files')
                request_body = GetJsonParams.for_keys_to_dict(*temp, my_dict=body)

                return self.post(**request_body).json(), out_values

        except SyntaxError:
            logger.log_warn('出错的问题数据是 => {}, 本次执行跳过请手动检查'.format(question))
        except TimeoutError:
            logger.log_warn('[WinError 10060] 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败')


if __name__ == '__main__':
    pass
