def _keywords(self):
        
        """ Returns the meta keywords in the page.
        """
        
        meta = self.find("meta", {"name":"keywords"})
        if isinstance(meta, dict) and \
           meta.has_key("content"):
            keywords = [k.strip() for k in meta["content"].split(",")]
        else:
            keywords = []
            
        return keywords