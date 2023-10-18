def parse_paragraphs(self, markup):
        
        """ Returns a list of paragraphs in the markup.
        
        A paragraph has a title and multiple lines of plain text.
        A paragraph might have parent and child paragraphs,
        denoting subtitles or bigger chapters.
        
        A paragraph might have links to additional articles.
        
        Formats numbered lists by replacing # by 1.
        Formats bulleted sublists like ** or *** with indentation.
        
        """
        
        # Paragraphs to exclude.
        refs = ["references", "notes", "notes and references", "external links", "further reading"]
        exclude = ["see also", "media", "gallery", "related topics", "lists", "gallery", "images"]
        exclude.extend(refs)
        
        paragraphs = []
        paragraph = WikipediaParagraph(self.title)
        paragraph_data = ""
        for chunk in markup.split("\n"):
            
            # Strip each line of whitespace, 
            # unless it's a preformatted line (starts with a space).
            if not chunk.startswith(" "):
                chunk = chunk.strip()
                
            # A title wrapped in "=", "==", "==="...
            # denotes a new paragraphs section.
            if chunk.startswith("="):

                if paragraph.title.lower() in refs \
                or (paragraph.parent and paragraph.parent.title.lower() in refs):
                    self.parse_paragraph_references(paragraph_data)
                paragraph.extend(self.parse_paragraph(paragraph_data))
                paragraphs.append(paragraph)
                
                # Initialise a new paragraph.
                # Create parent/child links to other paragraphs.
                title = chunk.strip().strip("=")
                title = self.plain(title)
                paragraph = WikipediaParagraph(title)
                paragraph.depth = self.parse_paragraph_heading_depth(chunk)
                if paragraph.title.lower() not in exclude:
                    paragraph = self.connect_paragraph(paragraph, paragraphs)
                paragraph_data = ""
            
            # Underneath a title might be links to in-depth articles,
            # e.g. Main articles: Computer program and Computer programming
            # which in wiki markup would be {{main|Computer program|Computer programming}}
            # The second line corrects" {{Main|Credit (finance)}} or {{Main|Usury}}".
            elif re.search(re.compile("^{{main", re.I), chunk):
                paragraph.main = [link.strip("} ") for link in chunk.split("|")[1:]]
                paragraph.main = [re.sub(re.compile("}}.*?{{main", re.I), "", link) 
                                  for link in paragraph.main]
                
            # At the bottom might be links to related articles,
            # e.g. See also: Abundance of the chemical elements
            # which in wiki markup would be {{see also|Abundance of the chemical elements}}
            elif re.search(re.compile("^{{see {0,1}also", re.I), chunk):
                paragraph.related = [link.strip("} ") for link in chunk.split("|")[1:]]
                
            # Accumulate the data in this paragraph,
            # we'll process it once a new paragraph starts.
            else:
                paragraph_data += chunk +"\n"
                
        # Append the last paragraph.
        if paragraph.title.lower() in refs \
        or (paragraph.parent and paragraph.parent.title.lower() in refs):
            self.parse_paragraph_references(paragraph_data)
        paragraph.extend(self.parse_paragraph(paragraph_data))
        paragraphs.append(paragraph)

        # The "See also" paragraph is an enumeration of links
        # which we already parsed so don't show them.
        # We also did references, and other paragraphs are not that relevant.        
        paragraphs_exclude = []
        for paragraph in paragraphs:
            if paragraph.title.lower() not in exclude \
            and not (paragraph.parent and paragraph.parent.title.lower() in exclude):
                paragraphs_exclude.append(paragraph)
        
        if len(paragraphs_exclude) == 1 and \
           len(paragraphs_exclude[0]) == 0:
            return []
        
        return paragraphs_exclude