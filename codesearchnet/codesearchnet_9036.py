def do_scan_range(self, line):
        """Do an ad-hoc scan of a range of points (group 1, variation 2, indexes 0-3). Command syntax is: scan_range"""
        self.application.master.ScanRange(opendnp3.GroupVariationID(1, 2), 0, 3, opendnp3.TaskConfig().Default())