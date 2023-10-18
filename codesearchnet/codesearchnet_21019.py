def adjust_previous(self, holidays_obj=None):
        """
        adjusts to Business Day Convention "Preceding" (4.12(a) (iii) 2006 ISDA Definitions).
        """
        while not BusinessDate.is_business_day(self, holidays_obj):
            self = BusinessDate.add_days(self, -1)
        return self