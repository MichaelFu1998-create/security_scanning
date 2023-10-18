def append_main_thread(self):
        """create & start main thread

        :return: None
        """
        thread = MainThread(main_queue=self.main_queue,
                            main_spider=self.main_spider,
                            branch_spider=self.branch_spider)
        thread.daemon = True
        thread.start()