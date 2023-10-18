def do_s2(self, line):
        """Send a SelectAndOperate BinaryOutput (group 12) CommandSet to the Outstation. Command syntax is: s2"""
        self.application.send_select_and_operate_command_set(opendnp3.CommandSet(
            [
                opendnp3.WithIndex(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_ON), 0)
            ]),
            command_callback
        )