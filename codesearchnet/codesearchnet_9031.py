def do_o3(self, line):
        """Send a DirectOperate BinaryOutput (group 12) CommandSet to the Outstation. Command syntax is: o3"""
        self.application.send_direct_operate_command_set(opendnp3.CommandSet(
            [
                opendnp3.WithIndex(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_ON), 0),
                opendnp3.WithIndex(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_OFF), 1)
            ]),
            command_callback
        )