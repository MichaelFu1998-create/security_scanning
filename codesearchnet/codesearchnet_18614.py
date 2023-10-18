def _build_regex(self):
        """
        Performs a reverse lookup on a named view and generates
        a list of regexes that match that object.  It generates
        regexes with the domain name included, using sites provided
        by the get_sites() method.
        
        >>> regex = provider.regex
        >>> regex.pattern
        'http://(www2.kusports.com|www2.ljworld.com|www.lawrence.com)/photos/(?P<year>\\d{4})/(?P<month>\\w{3})/(?P<day>\\d{1,2})/(?P<object_id>\\d+)/$'
        """
        # get the regexes from the urlconf
        url_patterns = resolver.reverse_dict.get(self._meta.named_view)
        
        try:
            regex = url_patterns[1]
        except TypeError:
            raise OEmbedException('Error looking up %s' % self._meta.named_view)
        
        # get a list of normalized domains
        cleaned_sites = self.get_cleaned_sites()
        
        site_regexes = []
        
        for site in self.get_sites():
            site_regexes.append(cleaned_sites[site.pk][0])
        
        # join the sites together with the regex 'or'
        sites = '|'.join(site_regexes)
        
        # create URL-matching regexes for sites
        regex = re.compile('(%s)/%s' % (sites, regex))
        
        return regex