def _process_current(self, handle, op, dest_path=None, dest_name=None):
        """Process current member with 'op' operation."""
        unrarlib.RARProcessFileW(handle, op, dest_path, dest_name)