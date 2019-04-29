# -*- coding:utf-8 -*-
import os
import time
import xlwt
import simplejson
from collections import Iterable
from lib.public import (
    http_hander, logger, text_similarity_comparison as JD)
from lib.utils import (
    make_report_template, operate_excel, time_setting, fp)
from lib.utils.get_json_params import GetJsonParams as GJ

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def run_test_cases(case_path):
    r"""Run the test case and generate data for the rendering template.

    :param case_path: Test case file path, str object.
    :return: generate data for the rendering template.
    :rtype: tuple object.
    """
    start = time_setting.timestamp('format_now')
    start_time = time.time()

    for file_content in fp.iter_files(os.path.join(BASE_PATH, case_path)):

        logger.log_debug('一共执行的测试集为{}'.format(file_content))

        results = []

        for filename, filepath in dict(file_content).items():

            logger.log_info('本次运行的用例为{} => {}'.format(filename, filepath))
            raw_list = operate_excel.read_excel(filepath)
            logger.log_debug(raw_list)
            for index, content in enumerate(raw_list):
                result = {}
                header = {}

                intent, expected_know = content['intent'], content['knowledge']
                quest = str(int(content['question'])) if isinstance(content['question'], float) else content['question']
                know = os.path.split(expected_know)[-1] if str(expected_know).find('.jpg') else expected_know

                logger.log_debug('当前问题是 => {}'.format(quest))

                try:
                    http = http_hander.BaseKeyWords()
                    res, out_head, out_text, out_image = http.make_test_templates({'question': quest})
                    res_texts = GJ.get_value(my_dict=res, key=out_text)
                    res_headers = GJ.get_value(my_dict=res, key=out_head)
                    res_images = GJ.get_value(my_dict=res, key=out_image)

                    logger.log_debug("问题:{},Text的值是->{} Header的值是->{} Image的值是->{}".\
                                     format(quest, res_texts, res_headers, res_images))

                    res_text, res_header, res_image = '', '', ''
                    if isinstance(res_texts, Iterable):
                        for text in res_texts:
                            res_text += text.strip()
                    if isinstance(res_headers, Iterable):
                        for head in res_headers:
                            res_header += head.strip()
                    if isinstance(res_images, Iterable):
                        for image in res_images:
                            res_image += os.path.split(image)[-1]

                    if not isinstance(res_texts, Iterable) and isinstance(res_headers, Iterable):
                        res_text = res_header
                    if not isinstance(res_texts, Iterable) and isinstance(res_images, Iterable):
                        res_text = res_image

                    if not isinstance(res_headers, Iterable) and not isinstance(res_texts, Iterable) and not isinstance(res_images, Iterable):
                        res_text = "answer.Text & answer.Header & answer.Image未返回任何值，机器人未根据意图查找出答案."

                except TypeError:
                    res_text = "Response Body is Null."
                except simplejson.errors.JSONDecodeError:
                    res_text = '抱歉，暂时没有相关的答案信息，我们已记录您的问题，感谢您的支持!'

                diff = JD.contrast_num(know, res_text)

                test_result = 'Pass' if diff > 0.7 else 'Fail'
                run = time.time()-start_time

                header.update({
                    'name': filename,
                    'start': start,
                    'run': run
                })

                result.update({
                    'question': quest,
                    'intent': intent,
                    'knowledge': know,
                    'response': res_text,
                    'diff': diff,
                    'result': test_result
                })

                results.append(result)
                make_report_template.create_test_report(filename, header, results)


# def write_result(case_path, method='Excel'):
#     """
#     Generate test reports
#     :param case_path: Test case file path, str object.
#     :param method: Type of test report generated, str object.
#     :return: None
#     """
#     for index, content in enumerate(run_test_cases(case_path)):
#         for filename, value in dict(content[index]).items():
#             header, results = value[0], value[1]
#
#             logger.log_debug('{}{}{}'.format(filename, header, results))
#
#             if method == 'Excel':
#                 workbook = xlwt.Workbook(encoding='utf-8')
#                 worksheet = workbook.add_sheet('sheet1')
#                 worksheet.write(0, 0, label='question')
#                 worksheet.write(0, 1, label='intent')
#                 worksheet.write(0, 2, label='knowledge')
#                 worksheet.write(0, 3, label='response')
#                 worksheet.write(0, 4, label='diff')
#                 worksheet.write(0, 5, label='result')
#                 val1 = 1
#                 val2 = 1
#                 val3 = 1
#                 val4 = 1
#                 val5 = 1
#                 val6 = 1
#                 col1 = worksheet.col(0)
#                 col1.width = 300 * 20
#                 col2 = worksheet.col(1)
#                 col2.width = 300 * 20
#                 col3 = worksheet.col(2)
#                 col3.width = 300 * 20
#                 col4 = worksheet.col(3)
#                 col4.width = 300 * 20
#                 col5 = worksheet.col(4)
#                 col5.width = 300 * 20
#                 col6 = worksheet.col(5)
#                 col6.width = 300 * 20
#                 style = xlwt.easyxf('align: wrap on')
#                 for list_item in results:
#                     for key, value in list_item.items():
#                         if key == "question":
#                             worksheet.write(val1, 0, value)
#                             val1 += 1
#                         elif key == "intent":
#                             worksheet.write(val2, 1, value)
#                             val2 += 1
#                         elif key == "knowledge":
#                             worksheet.write(val3, 2, value, style)
#                             val3 += 1
#                         elif key == "response":
#                             worksheet.write(val4, 3, value, style)
#                             val4 += 1
#                         elif key == 'diff':
#                             worksheet.write(val5, 4, value)
#                             val5 += 1
#                         elif key == 'result':
#                             worksheet.write(val6, 5, value)
#                             val6 += 1
#                 workbook.save('./report/report/{}.xlsx'.format(filename))
#             else:
#                 make_report_template.create_test_report(filename, header, results)


def main(filepath: str) -> None:
    r"""Run the program main entry

    :param filepath: Run file path, str object.
    :return: None
    """

    # Log files traceback
    for log_file in fp.iter_files('./report/log/'):
        for filename, filepath in dict(log_file).items():
            os.remove(filepath)

    # Report files traceback
    for report in fp.iter_files('./report/report/'):
        for report_name, report_path in dict(report).items():
            os.remove(report_path)

    run_test_cases(filepath)


if __name__ == '__main__':
    main('case')
