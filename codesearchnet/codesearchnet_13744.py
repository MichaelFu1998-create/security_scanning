def get_interval(x, intervals):
        """
        finds interval of the interpolation in which x lies.
        :param x:
        :param intervals: the interpolation intervals
        :return:
        """
        n = len(intervals)
        if n < 2:
            return intervals[0]
        n2 = n / 2
        if x < intervals[n2][0]:
            return spline.get_interval(x, intervals[:n2])
        else:
            return spline.get_interval(x, intervals[n2:])