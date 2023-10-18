def run(self, options):
        """
        In general, you don't need to overwrite this method.

        :param options:
        :return:
        """

        self.set_signal()
        self.check_exclusive_mode()

        slot = self.Handle(self)

        # start thread
        i = 0
        while i < options.threads:
            t = threading.Thread(target=self.worker, args=[slot])
            # only set daemon when once is False
            if options.once is True or options.no_daemon is True:
                t.daemon = False
            else:
                t.daemon = True

            t.start()
            i += 1

        # waiting thread
        if options.once is False:
            while True:
                if threading.active_count() > 1:
                    sleep(1)
                else:
                    if threading.current_thread().name == "MainThread":
                        sys.exit(0)

        pass