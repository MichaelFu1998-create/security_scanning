def connect_paragraph(self, paragraph, paragraphs):
        
        """ Create parent/child links to other paragraphs.
        
        The paragraphs parameters is a list of all the paragraphs
        parsed up till now.
        
        The parent is the previous paragraph whose depth is less.
        The parent's children include this paragraph.
        
        Called from parse_paragraphs() method.
        
        """

        if paragraph.depth > 0:
            n = range(len(paragraphs))
            n.reverse()
            for i in n:
                if paragraphs[i].depth == paragraph.depth-1:
                    paragraph.parent = paragraphs[i]
                    paragraphs[i].children.append(paragraph)
                    break
                    
        return paragraph