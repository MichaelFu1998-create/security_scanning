def close(self):
        """Close and exit the connection."""
        try:
            self.ssh.close()
            self.logger.debug("close connect succeed.")
        except paramiko.SSHException as e:
            self.unknown("close connect error: %s" % e)