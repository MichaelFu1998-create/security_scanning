def get_30_360(self, end):
        """
            implements 30/360 Day Count Convention (4.16(f) 2006 ISDA Definitions)
        """
        start_day = min(self.day, 30)
        end_day = 30 if (start_day == 30 and end.day == 31) else end.day
        return (360 * (end.year - self.year) + 30 * (end.month - self.month) + (end_day - start_day)) / 360.0