def Maximize(self, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """
        Set top level window maximize.
        """
        if self.IsTopLevel():
            return self.ShowWindow(SW.ShowMaximized, waitTime)
        return False