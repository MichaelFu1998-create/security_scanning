def detect_link_tag_time(self, tag):
        """
        Detect link, name and time for specified tag.

        :param dict tag: Tag data.
        :rtype: str, str, datetime
        :return: Link, name and time of the tag.
        """

        # if tag is nil - set current time
        newer_tag_time = self.get_time_of_tag(tag) if tag \
            else datetime.datetime.now()

        # if it's future release tag - set this value
        if tag["name"] == self.options.unreleased_label \
            and self.options.future_release:
            newer_tag_name = self.options.future_release
            newer_tag_link = self.options.future_release
        elif tag["name"] is not self.options.unreleased_label :
            # put unreleased label if there is no name for the tag
            newer_tag_name = tag["name"]
            newer_tag_link = newer_tag_name
        else:
            newer_tag_name = self.options.unreleased_label
            newer_tag_link = "HEAD"
        return [newer_tag_link, newer_tag_name, newer_tag_time]