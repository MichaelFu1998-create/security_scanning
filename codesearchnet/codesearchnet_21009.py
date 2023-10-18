def is_businessdate(in_date):
        """
        checks whether the provided date is a date
        :param BusinessDate, int or float in_date:
        :return bool:
        """
        # Note: if the data range has been created from pace_xl, then all the dates are bank dates
        # and here it remains to check the validity.
        # !!! However, if the data has been read from json string via json.load() function
        # it does not recognize that this numbers are bankdates, just considers them as integers
        # therefore, additional check is useful here, first to convert the date if it is integer to BusinessDate,
        # then check the validity.
        # (as the parameter to this method should always be a BusinessDate)
        if not isinstance(in_date, BaseDate):
            try:  # to be removed
                in_date = BusinessDate(in_date)
            except:
                return False
        y, m, d, = in_date.to_ymd()
        return is_valid_ymd(y, m, d)