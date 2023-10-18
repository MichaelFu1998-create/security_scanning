def parse_important(self, markup):
        
        """ Returns a list of words that appear in bold in the article.
        
        Things like table titles are not added to the list,
        these are probably bold because it makes the layout nice,
        not necessarily because they are important.
        
        """
        
        important = []
        table_titles = [table.title for table in self.tables]
        m = re.findall(self.re["bold"], markup)
        for bold in m:
            bold = self.plain(bold)
            if not bold in table_titles:
                important.append(bold.lower())
        
        return important