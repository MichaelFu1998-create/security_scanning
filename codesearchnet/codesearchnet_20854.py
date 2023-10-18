def get_urls(self):
        """
        Content of field ``856u42``. Typically URL pointing to producers
        homepage.

        Returns:
            list: List of URLs defined by producer.
        """
        urls = self.get_subfields("856", "u", i1="4", i2="2")

        return map(lambda x: x.replace("&amp;", "&"), urls)