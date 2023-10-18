def parse_table_row(self, markup, row):

        """ Parses a row of cells in a Wikipedia table.
        
        Cells in the row are separated by "||".
        A "!" indicates a row of heading columns.
        Each cell can contain properties before a "|",
        # e.g. align="right" | Cell 2 (right aligned).       
        
        """
        
        if row == None:
            row = WikipediaTableRow()
           
        markup = markup.replace("!!", "||")
        for cell in markup.lstrip("|!").split("||"):
            # The "|" after the properties can't be part of a link.
            i = cell.find("|")
            j = cell.find("[[")
            if i>0 and (j<0 or i<j):
                data = self.plain(cell[i+1:])
                properties = cell[:i].strip()
            else:
                data = self.plain(cell)
                properties = u""
            cell = WikipediaTableCell(data)
            cell.properties = properties
            row.append(cell)
        
        return row