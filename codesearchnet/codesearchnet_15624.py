def filter_merged_pull_requests(self, pull_requests):
        """
        This method filter only merged PR and fetch missing required
        attributes for pull requests. Using merged date is more correct
        than closed date.

        :param list(dict) pull_requests: Pre-filtered pull requests.
        :rtype: list(dict)
        :return:
        """

        if self.options.verbose:
            print("Fetching merge date for pull requests...")
        closed_pull_requests = self.fetcher.fetch_closed_pull_requests()

        if not pull_requests:
            return []
        pulls = copy.deepcopy(pull_requests)
        for pr in pulls:
            fetched_pr = None
            for fpr in closed_pull_requests:
                if fpr['number'] == pr['number']:
                    fetched_pr = fpr
            if fetched_pr:
                pr['merged_at'] = fetched_pr['merged_at']
                closed_pull_requests.remove(fetched_pr)

        for pr in pulls:
            if not pr.get('merged_at'):
                pulls.remove(pr)
        return pulls