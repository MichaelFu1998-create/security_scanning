def _description(self):
        
        """ Returns the meta description in the page.
        """        

        meta = self.find("meta", {"name":"description"})
        if isinstance(meta, dict) and \
           meta.has_key("content"):
            return meta["content"]
        else:
            return u""