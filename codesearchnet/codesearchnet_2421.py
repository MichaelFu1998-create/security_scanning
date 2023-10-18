def SendKeys(self, keys: str, interval: float = 0.01, waitTime: float = OPERATION_WAIT_TIME) -> None:
        """
        Make control have focus first and type keys.
        `self.SetFocus` may not work for some controls, you may need to click it to make it have focus.
        keys: str, keys to type, see the docstring of `SendKeys`.
        interval: float, seconds between keys.
        """
        self.SetFocus()
        SendKeys(keys, interval, waitTime)