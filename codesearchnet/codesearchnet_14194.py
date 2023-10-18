def parse_paragraph(self, markup):
        
        """ Creates a list from lines of text in a paragraph.
        
        Each line of text is a new item in the list,
        except lists and preformatted chunks (<li> and <pre>),
        these are kept together as a single chunk.
        
        Lists are formatted using parse_paragraph_list().
        
        Empty lines are stripped from the output.
        Indentation (i.e. lines starting with ":") is ignored.
        
        Called from parse_paragraphs() method.
        
        """
        
        s = self.plain(markup)
        # Add an extra linebreak between the last list item
        # and the normal line following after it, so they don't stick together, e.g.
        # **[[Alin Magic]], magic used in the videogame ''[[Rise of Nations: Rise of Legends]]''
        # In '''popular culture''':
        # * [[Magic (film)|''Magic'' (film)]], a 1978 film starring Anthony Hopkins and Ann-Margret
        s = re.sub(re.compile("\n([*#;].*?)\n([^*#?])", re.DOTALL), "\n\\1\n\n\\2", s)
        # This keeps list items with linebreaks 
        # between them nicely together.
        s = re.sub("\n{2,3}([*#;])", "\n\\1", s)
        chunks = []
        ch = ""
        i = 1
        for chunk in s.split("\n"):
            if chunk.startswith(":"):
                chunk = chunk.lstrip(":")
            if len(chunk.strip()) > 1:
                # Leave out taxoboxes and infoboxes.
                if not chunk.startswith("|"):
                    ch += chunk + "\n"
            if ch.strip() != "":
                if not re.search("^[ *#;]", chunk):
                    ch = self.parse_paragraph_list(ch)
                    chunks.append(ch.rstrip())
                    ch = ""

        if ch.strip() != "":
            ch = self.parse_paragraph_list(ch)
            chunks.append(ch.strip())
            
        return chunks