def auto_it_set_option(option, param):
    """
    Changes the operation of various AutoIt functions/parameters
    :param option: The option to change
    :param param: The parameter (varies by option).
    :return:
    """
    pre_value = AUTO_IT.AU3_AutoItSetOption(LPCWSTR(option), INT(param))
    return pre_value