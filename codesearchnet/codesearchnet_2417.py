def Hide(self, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """
        Call native `ShowWindow(SW.Hide)`.
        waitTime: float
        Return bool, True if succeed otherwise False.
        """
        return self.ShowWindow(SW.Hide, waitTime)