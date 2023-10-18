def fetch_events_async(self, issues, tag_name):
        """
        Fetch events for all issues and add them to self.events

        :param list issues: all issues
        :param str tag_name: name of the tag to fetch events for
        :returns: Nothing
        """

        if not issues:
            return issues

        max_simultaneous_requests = self.options.max_simultaneous_requests
        verbose = self.options.verbose
        gh = self.github
        user = self.options.user
        repo = self.options.project
        self.events_cnt = 0
        if verbose:
            print("fetching events for {} {}... ".format(
                len(issues), tag_name)
            )

        def worker(issue):
            page = 1
            issue['events'] = []
            while page > 0:
                rc, data = gh.repos[user][repo].issues[
                    issue['number']].events.get(
                    page=page, per_page=PER_PAGE_NUMBER)
                if rc == 200:
                    issue['events'].extend(data)
                    self.events_cnt += len(data)
                else:
                    self.raise_GitHubError(rc, data, gh.getheaders())
                page = NextPage(gh)

        threads = []
        cnt = len(issues)
        for i in range(0, (cnt // max_simultaneous_requests) + 1):
            for j in range(max_simultaneous_requests):
                idx = i * max_simultaneous_requests + j
                if idx == cnt:
                    break
                t = threading.Thread(target=worker, args=(issues[idx],))
                threads.append(t)
                t.start()
                if verbose > 2:
                    print(".", end="")
                    if not idx % PER_PAGE_NUMBER:
                        print("")
            for t in threads:
                t.join()
        if verbose > 2:
            print(".")