def do_write_time(self, line):
        """Write a TimeAndInterval to the Outstation. Command syntax is: write_time"""
        millis_since_epoch = int((datetime.now() - datetime.utcfromtimestamp(0)).total_seconds() * 1000.0)
        self.application.master.Write(opendnp3.TimeAndInterval(opendnp3.DNPTime(millis_since_epoch),
                                                               100,
                                                               opendnp3.IntervalUnits.Seconds),
                                      0,                            # index
                                      opendnp3.TaskConfig().Default())