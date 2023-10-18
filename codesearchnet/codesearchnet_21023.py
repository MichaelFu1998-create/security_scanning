def is_businessperiod(cls, in_period):
        """
        :param in_period: object to be checked
        :type in_period: object, str, timedelta
        :return: True if cast works
        :rtype: Boolean

        checks is argument con becasted to BusinessPeriod
        """
        try:  # to be removed
            if str(in_period).upper() == '0D':
                return True
            else:
                p = BusinessPeriod(str(in_period))
                return not (p.days == 0 and p.months == 0 and p.years == 0 and p.businessdays == 0)
        except:
            return False