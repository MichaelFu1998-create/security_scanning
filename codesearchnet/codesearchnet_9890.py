def exit(self):
        """Terminate gdb process
        Returns: None"""
        if self.gdb_process:
            self.gdb_process.terminate()
            self.gdb_process.communicate()
        self.gdb_process = None
        return None