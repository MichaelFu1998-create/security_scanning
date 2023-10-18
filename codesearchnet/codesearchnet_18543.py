def get_datetime_string(datetime_obj):
        '''
        Get datetime string from datetime object

        :param datetime datetime_obj: datetime object
        :return: datetime string
        :rtype: str
        '''

        if isinstance(datetime_obj, datetime):
            dft = DTFormat()
            return datetime_obj.strftime(dft.datetime_format)

        return None