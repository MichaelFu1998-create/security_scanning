def get_30E_360(self, end):
        """
        implements the 30E/360 Day Count Convention (4.16(g) 2006 ISDA Definitons)
        """

        y1, m1, d1 = self.to_ymd()
        # adjust to date immediately following the the last day
        y2, m2, d2 = end.add_days(0).to_ymd()

        d1 = min(d1, 30)
        d2 = min(d2, 30)

        return (360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)) / 360.0