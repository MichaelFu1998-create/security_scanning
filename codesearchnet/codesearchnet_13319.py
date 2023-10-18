def get_join_info(self):
        """If `self` is a MUC room join request return the information contained.

        :return: the join request details or `None`.
        :returntype: `MucX`
        """
        x=self.get_muc_child()
        if not x:
            return None
        if not isinstance(x,MucX):
            return None
        return x