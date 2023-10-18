def open(self):
        """Open the page.

        Navigates to :py:attr:`seed_url` and calls :py:func:`wait_for_page_to_load`.

        :return: The current page object.
        :rtype: :py:class:`Page`
        :raises: UsageError

        """
        if self.seed_url:
            self.driver_adapter.open(self.seed_url)
            self.wait_for_page_to_load()
            return self
        raise UsageError("Set a base URL or URL_TEMPLATE to open this page.")