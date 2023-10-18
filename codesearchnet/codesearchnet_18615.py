def provider_from_url(self, url):
        """
        Given a URL for any of our sites, try and match it to one, returning
        the domain & name of the match.  If no match is found, return current.
        
        Returns a tuple of domain, site name -- used to determine 'provider'
        """
        domain = get_domain(url)
        site_tuples = self.get_cleaned_sites().values()
        for domain_re, name, normalized_domain in site_tuples:
            if re.match(domain_re, domain):
                return normalized_domain, name
        site = Site.objects.get_current()
        return site.domain, site.name