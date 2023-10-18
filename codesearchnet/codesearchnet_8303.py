def find_next(self):
        """ Find the next url in the list
        """
        if int(self.num_retries) < 0:  # pragma: no cover
            self._cnt_retries += 1
            sleeptime = (self._cnt_retries - 1) * 2 if self._cnt_retries < 10 else 10
            if sleeptime:
                log.warning(
                    "Lost connection to node during rpcexec(): %s (%d/%d) "
                    % (self.url, self._cnt_retries, self.num_retries)
                    + "Retrying in %d seconds" % sleeptime
                )
                sleep(sleeptime)
            return next(self.urls)

        urls = [
            k
            for k, v in self._url_counter.items()
            if (
                # Only provide URLS if num_retries is bigger equal 0,
                # i.e. we want to do reconnects at all
                int(self.num_retries) >= 0
                # the counter for this host/endpoint should be smaller than
                # num_retries
                and v <= self.num_retries
                # let's not retry with the same URL *if* we have others
                # available
                and (k != self.url or len(self._url_counter) == 1)
            )
        ]
        if not len(urls):
            raise NumRetriesReached
        url = urls[0]
        return url