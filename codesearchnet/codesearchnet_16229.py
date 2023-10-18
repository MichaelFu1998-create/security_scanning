def UnPlug(self, force=False):
        """Unplug controller from Virtual USB Bus and free up ID"""
        if force:
            _xinput.UnPlugForce(c_uint(self.id))
        else:
            _xinput.UnPlug(c_uint(self.id))
        while self.id not in self.available_ids():
            if self.id == 0:
                break