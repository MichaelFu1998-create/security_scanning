def run(self, options):
        """
        .. todo::

            check network connection

        :param Namespace options: parse result from argparse
        :return:
        """
        self.logger.debug("debug enabled...")

        depends = ['git']
        nil_tools = []

        self.logger.info("depends list: %s", depends)

        for v in depends:
            real_path = shutil.which(v)
            if real_path:
                self.print_message("Found {}:{}..."
                                   "    {}".format(v,
                                                   real_path,
                                                   termcolor.colored(
                                                       '[OK]',
                                                       color='blue')))
            else:
                nil_tools.append(v)
                self.error_message(
                    'Missing tool:`{}`...    {}'.format(v, '[ERR]'), prefix='',
                    suffix='')

            pass

        if nil_tools:
            self.print_message('')
            self.error("please install missing tools...")
        else:
            self.print_message("\nNo error found,"
                               "you can use cliez in right way.")
            self.logger.debug("check finished...")
            pass

        pass