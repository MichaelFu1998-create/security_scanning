def do_disable_unsol(self, line):
        """Perform the function DISABLE_UNSOLICITED. Command syntax is: disable_unsol"""
        headers = [opendnp3.Header().AllObjects(60, 2),
                   opendnp3.Header().AllObjects(60, 3),
                   opendnp3.Header().AllObjects(60, 4)]
        self.application.master.PerformFunction("disable unsolicited",
                                                opendnp3.FunctionCode.DISABLE_UNSOLICITED,
                                                headers,
                                                opendnp3.TaskConfig().Default())