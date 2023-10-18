def do_scan_all(self, line):
        """Call ScanAllObjects. Command syntax is: scan_all"""
        self.application.master.ScanAllObjects(opendnp3.GroupVariationID(2, 1), opendnp3.TaskConfig().Default())