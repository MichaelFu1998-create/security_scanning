def parse_paragraph_references(self, markup):
        
        """ Updates references with content from specific paragraphs.
        
        The "references", "notes", "external links" paragraphs 
        are double-checked for references. Not all items in the list
        might have been referenced inside the article, or the item
        might contain more info than we initially parsed from it.
        
        Called from parse_paragraphs() method.
        
        """
        
        for chunk in markup.split("\n"):
            # We already parsed this, it contains the self.ref mark.
            # See if we can strip more notes from it.
            m = re.search(self.ref+"\(([0-9]*?)\)", chunk)
            if m:
                chunk = chunk.strip("* ")
                chunk = chunk.replace(m.group(0), "")
                chunk = self.plain(chunk)
                i = int(m.group(1))
                if chunk != "":
                    self.references[i-1].note = chunk
            # If it's not a citation we don't have this reference yet.
            elif chunk.strip().startswith("*") \
             and chunk.find("{{cite") < 0:
                chunk = chunk.strip("* ")
                chunk = self.plain(chunk)
                if chunk != "":
                    r = WikipediaReference()
                    r.note = chunk
                    self.references.append(r)