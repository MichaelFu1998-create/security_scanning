def system(self, cmd, fake_code=False):
        """
        a built-in wrapper make dry-run easier.
        you should use this instead use `os.system`

        .. note::

            to use it,you need add '--dry-run' option in
            your argparser options


        :param str cmd: command to execute
        :param bool fake_code: only display command
            when is True,default is False
        :return:
        """
        try:
            if self.options.dry_run:
                def fake_system(cmd):
                    self.print_message(cmd)
                    return fake_code

                return fake_system(cmd)
        except AttributeError:
            self.logger.warnning("fake mode enabled,"
                                 "but you don't set '--dry-run' option "
                                 "in your argparser options")
            pass

        return os.system(cmd)