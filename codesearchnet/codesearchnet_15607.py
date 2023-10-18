def generate_log_for_all_tags(self):
        """
        The full cycle of generation for whole project.

        :rtype: str
        :return: The complete change log for released tags.
        """

        if self.options.verbose:
            print("Generating log...")
        self.issues2 = copy.deepcopy(self.issues)

        log1 = ""
        if self.options.with_unreleased:
            log1 = self.generate_unreleased_section()

        log = ""
        for index in range(len(self.filtered_tags) - 1):
            log += self.do_generate_log_for_all_tags_part1(log, index)

        if self.options.tag_separator and log1:
            log = log1 + self.options.tag_separator + log
        else:
            log = log1 + log

        if len(self.filtered_tags) != 0:
            log += self.do_generate_log_for_all_tags_part2(log)

        return log