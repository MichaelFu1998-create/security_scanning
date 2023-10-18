def _parse(self):
        
        """ Strips links from the definition and gathers them in a links property.
        """
        
        p1 = "\[.*?\](.*?)\[\/.*?\]"
        p2 = "\[(.*?)\]"
        self.links = []
        for p in (p1,p2):
            for link in re.findall(p, self.description):
                self.links.append(link)
            self.description = re.sub(p, "\\1", self.description)
            
        self.description = self.description.strip()