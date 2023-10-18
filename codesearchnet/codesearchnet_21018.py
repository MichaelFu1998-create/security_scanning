def get_30E_360_ISDA(self, end):
        """
        implements the 30E/360 (ISDA) Day Count Convention (4.16(h) 2006 ISDA Definitions)
        :param end:
        :return:
        """
        y1, m1, d1 = self.to_ymd()
        # ajdust to date immediately following the last day
        y2, m2, d2 = end.add_days(0).to_ymd()

        if (m1 == 2 and d1 >= 28) or d1 == 31:
            d1 = 30
        if (m2 == 2 and d2 >= 28) or d2 == 31:
            d2 = 30

        return (360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)) / 360.0