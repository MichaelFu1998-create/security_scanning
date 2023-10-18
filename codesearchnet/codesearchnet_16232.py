def gamepad(self):
        """Returns the current gamepad state. Buttons pressed is shown as a raw integer value.
        Use rController.buttons for a list of buttons pressed.
        """
        state = _xinput_state()
        _xinput.XInputGetState(self.ControllerID - 1, pointer(state))
        self.dwPacketNumber = state.dwPacketNumber

        return state.XINPUT_GAMEPAD