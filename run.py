# -*- coding:utf-8 -*-
import os
import time

import xlwt

from lib.public import (
    http_hander, logger, text_similarity_comparison as json_diff)
from lib.utils import (
    make_report_template, operate_excel, time_setting, fp)
from lib.utils.get_json_params import GetJsonParams

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def run_test_cases(case_path):
    r"""Run the test case and generate data for the rendering template.

    :param case_path: Test case file path, str object.
    :return: generate data for the rendering template.
    :rtype: tuple object.
    """
    header = {}
    results = []
    res_sum = 0
    res_pass = 0
    res_fail = 0
    res_skip = 0
    start = time_setting.timestamp('format_now')
    start_time = time.time()

    for file_content in fp.iter_files(os.path.join(BASE_PATH, case_path)):

        raw_list = operate_excel.read_excel(file_content)
        for index, content in enumerate(raw_list):
            result = {}

            question, intent, knowledge = content['question'], content['intent'], content['knowledge']
            try:
                http = http_hander.BaseKeyWords()
                res, out_value = http.make_test_templates({'question': question})
                res_texts = GetJsonParams.get_value(my_dict=res, key=out_value)
                res_text = ''
                for text in res_texts:
                    res_text += text.strip()
            except TypeError:
                res_text = 'NoneType object is not subscriptable'

            expect, res = json_diff.count(knowledge), json_diff.count(res_text)
            merge_word = json_diff.merge_word(expect, res)
            v1, v2 = json_diff.cal_vector(expect, merge_word), json_diff.cal_vector(res, merge_word)
            diff = round(float(json_diff.cal_con_dis(v1, v2, len(merge_word))), 4)

            logger.log_info('{}{}{}'.format(expect, res, diff))

            if diff > 0.8:
                res_pass += 1
                test_result = 'pass'
            else:
                res_fail += 1
                test_result = 'fail'

            res_sum += 1
            run = time.time()-start_time

            header.update({
                'sum': res_sum,
                'pass': res_pass,
                'fail': res_fail,
                'skip': res_skip,
                'start': start,
                'run': run
            })

            result.update({
                'question': question,
                'intent': intent,
                'knowledge': knowledge,
                'response': res_text,
                'diff': diff,
                'result': test_result
            })

            results.append(result)
        return header, results


def write_result(case_path, method='Excel'):
    """
    Generate test reports
    :param case_path: Test case file path, str object.
    :param method: Type of test report generated, str object.
    :return: None
    """
    header, results = run_test_cases(case_path)
    if method == 'Excel':
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('sheet1')
        worksheet.write(0, 0, label='question')
        worksheet.write(0, 1, label='intent')
        worksheet.write(0, 2, label='knowledge')
        worksheet.write(0, 3, label='response')
        worksheet.write(0, 4, label='diff')
        worksheet.write(0, 5, label='result')
        val1 = 1
        val2 = 1
        val3 = 1
        val4 = 1
        val5 = 1
        val6 = 1
        col1 = worksheet.col(0)
        col1.width = 300 * 20
        col2 = worksheet.col(1)
        col2.width = 300 * 20
        col3 = worksheet.col(2)
        col3.width = 300 * 20
        col4 = worksheet.col(3)
        col4.width = 300 * 20
        col5 = worksheet.col(4)
        col5.width = 300 * 20
        col6 = worksheet.col(5)
        col6.width = 300 * 20
        style = xlwt.easyxf('align: wrap on')
        for list_item in results:
            for key, value in list_item.items():
                if key == "question":
                    worksheet.write(val1, 0, value)
                    val1 += 1
                elif key == "intent":
                    worksheet.write(val2, 1, value)
                    val2 += 1
                elif key == "knowledge":
                    worksheet.write(val3, 2, value, style)
                    val3 += 1
                elif key == "response":
                    worksheet.write(val4, 3, value, style)
                    val4 += 1
                elif key == 'diff':
                    worksheet.write(val5, 4, value)
                    val5 += 1
                elif key == 'result':
                    worksheet.write(val6, 5, value)
                    val6 += 1
        workbook.save('./report/BotChatTestReport.xlsx')
    else:
        make_report_template.create_test_report(header, results)


if __name__ == '__main__':
    for log_file in fp.iter_files('./report/log/'):
        os.remove(log_file)
    write_result(case_path='work_flow', method='html')
