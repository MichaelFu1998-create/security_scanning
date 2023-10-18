def get_free_space(self):
        """
        Return free space in bytes.
        """
        cmd = "df -k | grep -vE '^Filesystem|tmpfs|cdrom|none|udev|cgroup' | awk '{ print($1 \" \" $4 }'"
        lines = [_ for _ in self.run(cmd).strip().split('\n') if _.startswith('/')]
        assert len(lines) == 1, 'Ambiguous devices: %s' % str(lines)
        device, kb = lines[0].split(' ')
        free_space = int(kb) * 1024
        self.vprint('free_space (bytes):', free_space)
        return free_space