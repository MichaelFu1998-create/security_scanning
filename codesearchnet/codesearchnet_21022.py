def adjust_mod_previous(self, holidays_obj=None):
        """
        ajusts to Business Day Convention "Modified Preceding" (not in 2006 ISDA Definitons).
        """
        month = self.month
        new = BusinessDate.adjust_previous(self, holidays_obj)
        if month != new.month:
            new = BusinessDate.adjust_follow(self, holidays_obj)
        self = new
        return self