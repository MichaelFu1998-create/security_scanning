def disk(self):
        """
        Display percent of disk usage.
        """
        r = self.local_renderer
        r.run(r.env.disk_usage_command)