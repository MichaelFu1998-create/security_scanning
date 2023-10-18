def set_date_from_event(self, event, issue):
        """
        Set closed date from this issue.

        :param dict event: event data
        :param dict issue: issue data
        """

        if not event.get('commit_id', None):
            issue['actual_date'] = timestring_to_datetime(issue['closed_at'])
            return
        try:
            commit = self.fetcher.fetch_commit(event)
            issue['actual_date'] = timestring_to_datetime(
                commit['author']['date']
            )
        except ValueError:
            print("WARNING: Can't fetch commit {0}. "
                  "It is probably referenced from another repo.".
                  format(event['commit_id']))
            issue['actual_date'] = timestring_to_datetime(issue['closed_at'])