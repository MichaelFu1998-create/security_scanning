def Show(self, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """
        Call native `ShowWindow(SW.Show)`.
        Return bool, True if succeed otherwise False.
        """
        return self.ShowWindow(SW.Show, waitTime)