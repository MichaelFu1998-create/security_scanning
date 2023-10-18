def parse_disambiguation(self, markup):
        
        """ Gets the Wikipedia disambiguation page for this article.
        
        A Wikipedia disambiguation link refers to other pages
        with the same title but of smaller significance,
        e.g. {{dablink|For the IEEE magazine see [[Computer (magazine)]].}}
        
        """
        
        m = re.search(self.re["disambiguation"], markup)
        if m:
            return self.parse_links(m.group(1))
        else:
            return []