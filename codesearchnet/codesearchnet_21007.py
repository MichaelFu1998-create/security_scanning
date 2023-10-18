def from_string(date_str):
        """
        construction from the following string patterns
        '%Y-%m-%d'
        '%d.%m.%Y'
        '%m/%d/%Y'
        '%Y%m%d'

        :param str date_str:
        :return BusinessDate:
        """
        if date_str.count('-'):
            str_format = '%Y-%m-%d'
        elif date_str.count('.'):
            str_format = '%d.%m.%Y'
        elif date_str.count('/'):
            str_format = '%m/%d/%Y'
        elif len(date_str) == 8:
            str_format = '%Y%m%d'
        elif len(date_str) == 4:
            year = ord(date_str[0]) * 256 + ord(date_str[1])
            month = ord(date_str[2])
            day = ord(date_str[3])
            return BusinessDate.from_ymd(year, month, day)
        else:
            msg = "the date string " + date_str + " has not the right format"
            raise ValueError(msg)

        d = datetime.strptime(date_str, str_format)

        return BusinessDate.from_ymd(d.year, d.month, d.day)