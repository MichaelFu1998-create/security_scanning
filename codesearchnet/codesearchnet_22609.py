def run(self):
        """run your main spider here
        as for branch spider result data, you can return everything or do whatever with it
        in your own code

        :return: None
        """
        config = config_creator()
        debug = config.debug
        branch_thread_sleep = config.branch_thread_sleep
        while 1:
            url = self.branch_queue.get()
            if debug:
                print('branch thread-{} start'.format(url))
            branch_spider = self.branch_spider(url)
            sleep(random.randrange(*branch_thread_sleep))
            branch_spider.request_page()
            if debug:
                print('branch thread-{} end'.format(url))
            self.branch_queue.task_done()