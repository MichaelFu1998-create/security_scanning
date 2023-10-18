def adjust_follow(self, holidays_obj=None):
        """
        adjusts to Business Day Convention "Following" (4.12(a) (i) 2006 ISDA Definitions).
        """
        while not BusinessDate.is_business_day(self, holidays_obj):
            self = BusinessDate.add_days(self, 1)
        return self