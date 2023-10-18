def datetime_str_to_timestamp(datetime_str):
        '''
        '2018-01-01 00:00:00' (str) --> 1514736000

        :param str datetime_str: datetime string
        :return: unix timestamp (int) or None
        :rtype: int or None
        '''

        try:
            dtf = DTFormat()
            struct_time = time.strptime(datetime_str, dtf.datetime_format)
            return time.mktime(struct_time)
        except:
            return None