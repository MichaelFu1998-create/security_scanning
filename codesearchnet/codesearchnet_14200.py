def connect_table(self, table, chunk, markup):

        """ Creates a link from the table to paragraph and vice versa.
        
        Finds the first heading above the table in the markup.
        This is the title of the paragraph the table belongs to.
        
        """

        k = markup.find(chunk)
        i = markup.rfind("\n=", 0, k)
        j = markup.find("\n", i+1)
        paragraph_title = markup[i:j].strip().strip("= ")
        for paragraph in self.paragraphs:
            if paragraph.title == paragraph_title:
                paragraph.tables.append(table)
                table.paragraph = paragraph