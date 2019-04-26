# -*- coding:utf-8 -*-
from lib.utils import operate_excel


def load_data_source():

    knowledge_data = operate_excel.read_excel(r'F:\BotChatContrast\data_source\knowledge_base\交通.xlsx')
    train_data = operate_excel.read_excel(r'F:\BotChatContrast\data_source\training_set\交通.xlsx')

    case_data, cases_data = {}, []
    for tr_index, tr_content in enumerate(train_data):
        print(tr_content)
        for tr_key, tr_value in tr_content.items:
            for kn_index, kn_content in enumerate(knowledge_data):
                for kn_key, kn_value in kn_content.items:
                    if tr_key == kn_key:
                        tr_content['router'] = kn_value
                    else:
                        tr_content[tr_key] = tr_value
                    case_data.update(tr_content)
    cases_data.append(case_data)
    return cases_data


if __name__ == '__main__':
    print(load_data_source())
