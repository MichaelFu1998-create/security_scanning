def generate_sub_section(self, issues, prefix):
        """
        Generate formated list of issues for changelog.

        :param list issues: Issues to put in sub-section.
        :param str prefix: Title of sub-section.
        :rtype: str
        :return: Generated ready-to-add sub-section.
        """

        log = ""
        if issues:
            if not self.options.simple_list:
                log += u"{0}\n\n".format(prefix)
            for issue in issues:
                merge_string = self.get_string_for_issue(issue)
                log += u"- {0}\n".format(merge_string)
            log += "\n"
        return log