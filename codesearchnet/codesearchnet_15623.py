def get_filtered_pull_requests(self, pull_requests):
        """
        This method fetches missing params for PR and filter them
        by specified options. It include add all PR's with labels
        from options.include_labels and exclude all from
        options.exclude_labels.

        :param list(dict) pull_requests: All pull requests.
        :rtype: list(dict)
        :return: Filtered pull requests.
        """

        pull_requests = self.filter_by_labels(pull_requests, "pull requests")
        pull_requests = self.filter_merged_pull_requests(pull_requests)
        if self.options.verbose > 1:
            print("\tremaining pull requests: {}".format(len(pull_requests)))
        return pull_requests