def get_internal_urls(self):
        """
        URL's, which may point to edeposit, aleph, kramerius and so on.

        Fields ``856u40``, ``998a`` and ``URLu``.

        Returns:
            list: List of internal URLs. 
        """
        internal_urls = self.get_subfields("856", "u", i1="4", i2="0")
        internal_urls.extend(self.get_subfields("998", "a"))
        internal_urls.extend(self.get_subfields("URL", "u"))

        return map(lambda x: x.replace("&amp;", "&"), internal_urls)