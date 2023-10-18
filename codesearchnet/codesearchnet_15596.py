def fetch_events_for_issues_and_pr(self):
        """
        Fetch event for issues and pull requests

        @return [Array] array of fetched issues
        """

        # Async fetching events:
        self.fetcher.fetch_events_async(self.issues, "issues")
        self.fetcher.fetch_events_async(self.pull_requests, "pull requests")