def set_value(self, control, value=None):
        """Set a value on the controller
    If percent is True all controls will accept a value between -1.0 and 1.0

    If not then:
        Triggers are 0 to 255
        Axis are -32768 to 32767

    Control List:
        AxisLx          , Left Stick X-Axis
        AxisLy          , Left Stick Y-Axis
        AxisRx          , Right Stick X-Axis
        AxisRy          , Right Stick Y-Axis
        BtnBack         , Menu/Back Button
        BtnStart        , Start Button
        BtnA            , A Button
        BtnB            , B Button
        BtnX            , X Button
        BtnY            , Y Button
        BtnThumbL       , Left Thumbstick Click
        BtnThumbR       , Right Thumbstick Click
        BtnShoulderL    , Left Shoulder Button
        BtnShoulderR    , Right Shoulder Button
        Dpad            , Set Dpad Value (0 = Off, Use DPAD_### Constants)
        TriggerL        , Left Trigger
        TriggerR        , Right Trigger

    """
        func = getattr(_xinput, 'Set' + control)

        if 'Axis' in control:
            target_type = c_short

            if self.percent:
                target_value = int(32767 * value)
            else:
                target_value = value
        elif 'Btn' in control:
            target_type = c_bool
            target_value = bool(value)
        elif 'Trigger' in control:
            target_type = c_byte

            if self.percent:
                target_value = int(255 * value)
            else:
                target_value = value
        elif 'Dpad' in control:
            target_type = c_int
            target_value = int(value)

        func(c_uint(self.id), target_type(target_value))