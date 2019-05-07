# -*- coding:utf-8 -*-


class GetJsonParams(object):

    @classmethod
    def get_value(cls, my_dict: dict, key: str) -> str:
        r"""Parses a nested dictionary and gets the value of the specified key.

        :param my_dict: A dictionary to be parsed, dict object.
        :param key: Specifies the key to resolve, str object.
        :return: Gets the specified value for Json.
        :rtype: str object.
        """

        if isinstance(my_dict, dict):
            if my_dict.get(key) or my_dict.get(key) == 0 or my_dict.get(key) == ''\
                    and my_dict.get(key) is False or my_dict.get(key) == []:
                return my_dict.get(key)

            for my_dict_key in my_dict:
                if cls.get_value(my_dict.get(my_dict_key), key) or \
                                cls.get_value(my_dict.get(my_dict_key), key) is False:
                    return cls.get_value(my_dict.get(my_dict_key), key)

        if isinstance(my_dict, list):
            for my_dict_arr in my_dict:
                if cls.get_value(my_dict_arr, key) \
                        or cls.get_value(my_dict_arr, key) is False:
                    return cls.get_value(my_dict_arr, key)

    @classmethod
    def for_keys_to_dict(cls, *args: tuple, my_dict: dict) -> dict:
        r"""Specifies multiple keys and retrieves multiple corresponding keys of a dictionary to form a new dictionary.

        :param args: The specified key, tuple object.
        :param my_dict: A dictionary to be parsed, dict object.
        :return: The new dictionary after parsing.
        :rtype: dict object.
        """
        result = {}
        if len(args) > 0:
            for key in args:
                result.update({key: cls.get_value(my_dict, str(key))})
        return result


if __name__ == '__main__':
    data = {"status":1,"answer":{"Header":None,"Text":None,"ImageUrl":[],"VideoUrl":None,"Footer":None},"context":{"Header":["请问您想咨询的是以下哪种情形："],"Content":[{"Value":"1.逾期","Type":"header"},{"Value":"2.未逾期（自退工之日起30天内）","Type":"header"}],"Footer":[]},"responseType":"2","categoryid":None}
    con = GetJsonParams.get_value(data, 'Content')
    for val in con:
        print(dict(val)['Value'])

