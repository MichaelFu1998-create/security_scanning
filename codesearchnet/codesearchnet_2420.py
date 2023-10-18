def SendKey(self, key: int, waitTime: float = OPERATION_WAIT_TIME) -> None:
        """
        Make control have focus first and type a key.
        `self.SetFocus` may not work for some controls, you may need to click it to make it have focus.
        key: int, a key code value in class Keys.
        waitTime: float.
        """
        self.SetFocus()
        SendKey(key, waitTime)