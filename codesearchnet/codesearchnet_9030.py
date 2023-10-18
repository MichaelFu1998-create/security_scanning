def do_o1(self, line):
        """Send a DirectOperate BinaryOutput (group 12) index 5 LATCH_ON to the Outstation. Command syntax is: o1"""
        self.application.send_direct_operate_command(opendnp3.ControlRelayOutputBlock(opendnp3.ControlCode.LATCH_ON),
                                                     5,
                                                     command_callback)