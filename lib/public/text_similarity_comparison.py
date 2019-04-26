# -*- coding:utf-8 -*-
import jieba
from collections import Counter
import numpy as np
import math


def stopwords(seg_list: list) -> list:
    r"""Filter out stop words.

    :param seg_list: The list obtained after word segmentation, list object.
    :return: Remove the data after the stop word.
    :rtype: list object.
    """

    stayed_word = []

    filter_keywords = open(r'./data/stopKeywords', 'r', encoding='utf-8')
    stop_key = [line.strip() for line in filter_keywords.readlines()]
    for word in seg_list:
        if word not in stop_key:
            stayed_word.append(word)
    return stayed_word


def count(res: str):
    r"""Keyword statistics and word frequency statistics.

    :param res: Keywords, str object.
    :return: Returns keyword and word frequency statistics.
    :rtype: list object.
    """

    seg_list = list(jieba.cut(res))
    seg_list = stopwords(seg_list)
    dic = Counter(seg_list)

    return (dic)


def merge_word(expect: dict, res: dict) -> list:
    r"""Keyword merge diversity.

    :param expect: The expected data, dict object.
    :param res: Actual return result, dict object.
    :return: And set the results.
    :rtype: list object.
    """
    return list(set(list(expect.keys())).union(set(list(res.keys()))))


def cal_vector(expect: dict, merge_word: list) -> list:
    r"""Get the document vector

    :param expect: The expected data, dict object.
    :param merge_word: Keyword merge diversity, list object.
    :return: Get the vector result.
    :rtype: list object.
    """
    vector = []
    for ch in merge_word:
        if ch in expect:
            vector.append(expect[ch])
        else:
            vector.append(0)
    return vector


def cal_con_dis(v1: list, v2: list, length_vector):
    r"""Compute cosine distance.

    :param v1: Expected vector, list object.
    :param v2: The actual vector, list object.
    :param length_vector: The length of the vector, list object.
    :return: Degree of contrast.
    :rtype: float object.
    """

    a1 = np.asarray(v1)
    a2 = np.asarray(v2)
    A = math.sqrt(np.sum(a1**2)) * math.sqrt(np.sum(a1**2))
    B = np.sum(a1 * a2)

    try:
        return format(float(B) / A, ".3f")
    except ZeroDivisionError:
        return 0


if __name__ == '__main__':
    pass
