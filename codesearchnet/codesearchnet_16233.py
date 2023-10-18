def buttons(self):
        """Returns a list of buttons currently pressed"""
        return [name for name, value in rController._buttons.items()
                if self.gamepad.wButtons & value == value]