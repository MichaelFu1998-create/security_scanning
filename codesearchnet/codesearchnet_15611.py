def generate_log_for_tag(self,
                             pull_requests,
                             issues,
                             newer_tag,
                             older_tag_name):
        """
        Generates log for tag section with header and body.

        :param list(dict) pull_requests: List of PR's in this tag section.
        :param list(dict) issues: List of issues in this tag section.
        :param dict newer_tag: Github data of tag for this section.
        :param str older_tag_name: Older tag, used for the links.
                                   May be special value, if **newer tag** is
                                   the first tag. (Means **older_tag** is when
                                   the repo was created.)
        :rtype: str
        :return: Ready-to-add and parsed tag section.
        """

        newer_tag_link, newer_tag_name, \
        newer_tag_time = self.detect_link_tag_time(newer_tag)

        github_site = "https://github.com" or self.options.github_endpoint
        project_url = "{0}/{1}/{2}".format(
            github_site, self.options.user, self.options.project)

        log = self.generate_header(newer_tag_name, newer_tag_link,
                                   newer_tag_time, older_tag_name, project_url)
        if self.options.issues:
            # Generate issues:
            log += self.issues_to_log(issues, pull_requests)
        if self.options.include_pull_request:
            # Generate pull requests:
            log += self.generate_sub_section(
                pull_requests, self.options.merge_prefix
            )
        return log