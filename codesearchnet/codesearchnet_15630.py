def get_temp_tag_for_repo_creation(self):
        """
        If not already cached, fetch the creation date of the repo, cache it
        and return the special value indicating the creation of the repo.

        :rtype: str
        :return: value indicating the creation
        """
        tag_date = self.tag_times_dict.get(REPO_CREATED_TAG_NAME, None)
        if not tag_date:
            tag_name, tag_date = self.fetcher.fetch_repo_creation_date()
            self.tag_times_dict[tag_name] = timestring_to_datetime(tag_date)
        return REPO_CREATED_TAG_NAME