def links(self, external=True):
        
        """ Retrieves links in the page.
        
        Returns a list of URL's.
        By default, only external URL's are returned.
        External URL's starts with http:// and point to another
        domain than the domain the page is on.
        
        """
        
        domain = URLParser(self.url).domain
        
        links = []
        for a in self("a"):
            for attribute, value in a.attrs:
                if attribute == "href":
                    if not external \
                    or (value.startswith("http://") and value.find("http://"+domain) < 0):
                        links.append(value)
                        
        return links