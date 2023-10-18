def compound_changelog(self):
        """
        Main function to start change log generation

        :rtype: str
        :return: Generated change log file
        """

        self.fetch_and_filter_tags()
        tags_sorted = self.sort_tags_by_date(self.filtered_tags)
        self.filtered_tags = tags_sorted
        self.fetch_and_filter_issues_and_pr()

        log = str(self.options.frontmatter) \
            if self.options.frontmatter else u""
        log += u"{0}\n\n".format(self.options.header)

        if self.options.unreleased_only:
            log += self.generate_unreleased_section()
        else:
            log += self.generate_log_for_all_tags()

        try:
            with open(self.options.base) as fh:
                log += fh.read()
        except (TypeError, IOError):
            pass
        return log