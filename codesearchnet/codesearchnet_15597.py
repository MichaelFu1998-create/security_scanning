def fetch_tags_dates(self):
        """ Async fetching of all tags dates. """

        if self.options.verbose:
            print(
                "Fetching dates for {} tags...".format(len(self.filtered_tags))
            )

        def worker(tag):
            self.get_time_of_tag(tag)

        # Async fetching tags:
        threads = []
        max_threads = 50
        cnt = len(self.filtered_tags)
        for i in range(0, (cnt // max_threads) + 1):
            for j in range(max_threads):
                idx = i * 50 + j
                if idx == cnt:
                    break
                t = threading.Thread(target=worker,
                                     args=(self.filtered_tags[idx],))
                threads.append(t)
                t.start()
                if self.options.verbose > 2:
                    print(".", end="")
            for t in threads:
                t.join()
        if self.options.verbose > 2:
            print(".")
        if self.options.verbose > 1:
            print("Fetched dates for {} tags.".format(
                len(self.tag_times_dict))
            )