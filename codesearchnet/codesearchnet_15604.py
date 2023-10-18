def generate_header(self, newer_tag_name, newer_tag_link,
                        newer_tag_time,
                        older_tag_link, project_url):
        """
        Generate a header for a tag section with specific parameters.

        :param str newer_tag_name: Name (title) of newer tag.
        :param str newer_tag_link: Tag name of newer tag, used for links.
                               Could be same as **newer_tag_name** or some
                               specific value, like `HEAD`.
        :param datetime newer_tag_time: Date and time when
                                        newer tag was created.
        :param str older_tag_link: Tag name of older tag, used for links.
        :param str project_url: URL for current project.
        :rtype: str
        :return: Generated ready-to-add tag section.
        """

        log = ""
        # Generate date string:
        # noinspection PyUnresolvedReferences
        time_string = newer_tag_time.strftime(self.options.date_format)

        # Generate tag name and link
        if self.options.release_url:
            release_url = self.options.release_url.format(newer_tag_link)
        else:
            release_url = u"{project_url}/tree/{newer_tag_link}".format(
                project_url=project_url, newer_tag_link=newer_tag_link)

        if not self.options.unreleased_with_date and \
                newer_tag_name == self.options.unreleased_label:
            log += u"## [{newer_tag_name}]({release_url})\n\n".format(
                newer_tag_name=newer_tag_name, release_url=release_url)
        else:
            log += u"## [{newer_tag_name}]({release_url}) " \
                   u"({time_string})\n".format(
                        newer_tag_name=newer_tag_name,
                        release_url=release_url,
                        time_string=time_string
                   )

        if self.options.compare_link \
            and older_tag_link != REPO_CREATED_TAG_NAME:
            # Generate compare link
            log += u"[Full Changelog]"
            log += u"({project_url}/compare/{older_tag_link}".format(
                project_url=project_url,
                older_tag_link=older_tag_link,
            )
            log += u"...{newer_tag_link})\n\n".format(
                newer_tag_link=newer_tag_link
            )
        return log