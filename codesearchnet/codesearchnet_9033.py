def do_s1(self, line):
        """Send a SelectAndOperate BinaryOutput (group 12) index 8 LATCH_ON to the Outstation. Command syntax is: s1"""
        self.application.send_select_and_operate_command(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_ON),
                                                         8,
                                                         command_callback)