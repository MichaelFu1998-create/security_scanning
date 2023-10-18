def sys_newuname(self, old_utsname):
        """
        Writes system information in the variable C{old_utsname}.
        :rtype: int
        :param old_utsname: the buffer to write the system info.
        :return: C{0} on success
        """
        from datetime import datetime

        def pad(s):
            return s + '\x00' * (65 - len(s))

        now = datetime(2017, 8, 0o1).strftime("%a %b %d %H:%M:%S ART %Y")
        info = (('sysname', 'Linux'),
                ('nodename', 'ubuntu'),
                ('release', '4.4.0-77-generic'),
                ('version', '#98 SMP ' + now),
                ('machine', self._uname_machine),
                ('domainname', ''))

        uname_buf = ''.join(pad(pair[1]) for pair in info)
        self.current.write_bytes(old_utsname, uname_buf)
        return 0