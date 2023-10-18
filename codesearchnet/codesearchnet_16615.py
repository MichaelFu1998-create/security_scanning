def ping(self):
        """
        Sending ICMP packets.

        :return: ``ping`` command execution result.
        :rtype: :py:class:`.PingResult`
        :raises ValueError: If parameters not valid.
        """

        self.__validate_ping_param()

        ping_proc = subprocrunner.SubprocessRunner(self.__get_ping_command())
        ping_proc.run()

        return PingResult(ping_proc.stdout, ping_proc.stderr, ping_proc.returncode)