def connect(self, interactive=False):
        """
        Open SSH connection to droplet

        Parameters
        ----------
        interactive: bool, default False
            If True then SSH client will prompt for password when necessary
            and also print output to console
        """
        from poseidon.ssh import SSHClient
        rs = SSHClient(self.ip_address, interactive=interactive)
        return rs