def generate_unreleased_section(self):
        """
        Generate log for unreleased closed issues.

        :rtype: str
        :return: Generated ready-to-add unreleased section.
        """
        if not self.filtered_tags:
            return ""
        now = datetime.datetime.utcnow()
        now = now.replace(tzinfo=dateutil.tz.tzutc())
        head_tag = {"name": self.options.unreleased_label}
        self.tag_times_dict[head_tag["name"]] = now
        unreleased_log = self.generate_log_between_tags(
            self.filtered_tags[0], head_tag)
        return unreleased_log