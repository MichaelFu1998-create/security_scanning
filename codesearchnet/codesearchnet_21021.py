def adjust_mod_follow(self, holidays_obj=None):
        """
        adjusts to Business Day Convention "Modified [Following]" (4.12(a) (ii) 2006 ISDA Definitions).
        """
        month = self.month
        new = BusinessDate.adjust_follow(self, holidays_obj)
        if month != new.month:
            new = BusinessDate.adjust_previous(self, holidays_obj)
        self = new
        return self