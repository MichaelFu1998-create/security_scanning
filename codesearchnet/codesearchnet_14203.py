def parse_categories(self, markup):
        
        """ Returns a list of categories the page belongs to.

        # A Wikipedia category link looks like:
        # [[Category:Computing]]
        # This indicates the page is included in the given category.
        # If "Category" is preceded by ":" this indicates a link to a category.
        
        """
        
        categories = []
        m = re.findall(self.re["category"], markup)
        for category in m:
            category = category.split("|")
            page = category[0].strip()
            display = u""
            if len(category) > 1: 
                display = category[1].strip()
            #if not categories.has_key(page):
            #    categories[page] = WikipediaLink(page, u"", display)
            if not page in categories:
                categories.append(page)
                
        return categories