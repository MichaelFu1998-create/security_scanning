def run(self):
        """run your main spider here, and get a list/tuple of url as result
        then make the instance of branch thread

        :return: None
        """
        global existed_urls_list
        config = config_creator()
        debug = config.debug
        main_thread_sleep = config.main_thread_sleep
        branch_thread_num = config.branch_thread_num
        while 1:
            url = self.main_queue.get()
            if debug:
                print('main thread-{} start'.format(url))
            main_spider = self.main_spider(url)
            sleep(random.randrange(*main_thread_sleep))
            links = main_spider.request_urls()

            try:
                assert type(links) in VALIDATE_URLS
            except AssertionError:
                error_message('except to return a list or tuple which contains url')
                links = list()

            branch_queue = queue.Queue(branch_thread_num)

            for i in range(branch_thread_num):
                branch_thread = BranchThread(branch_queue=branch_queue,
                                             branch_spider=self.branch_spider)
                branch_thread.daemon = True
                branch_thread.start()

            for link in links:
                if link not in existed_urls_list:
                    existed_urls_list.append(link)
                    branch_queue.put(link)

            branch_queue.join()
            if debug:
                print('main thread-{}\'s child threads is all finish'.format(url))
            self.main_queue.task_done()