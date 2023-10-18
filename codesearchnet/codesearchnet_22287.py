def print_loading(self, wait, message):
        """
        print loading message on screen

        .. note::

            loading message only write to `sys.stdout`


        :param int wait: seconds to wait
        :param str message: message to print
        :return: None
        """
        tags = ['\\', '|', '/', '-']

        for i in range(wait):
            time.sleep(0.25)
            sys.stdout.write("%(message)s... %(tag)s\r" % {
                'message': message,
                'tag': tags[i % 4]
            })

            sys.stdout.flush()
            pass

        sys.stdout.write("%s... Done...\n" % message)
        sys.stdout.flush()
        pass