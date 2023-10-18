def convert_table(self, markup):
        
        """ Subtitutes <table> content to Wikipedia markup.
        """
        
        for table in re.findall(self.re["html-table"], markup):
            wiki = table
            wiki = re.sub(r"<table(.*?)>", "{|\\1", wiki)
            wiki = re.sub(r"<tr(.*?)>", "|-\\1", wiki)
            wiki = re.sub(r"<td(.*?)>", "|\\1|", wiki)
            wiki = wiki.replace("</td>", "\n")
            wiki = wiki.replace("</tr>", "\n")
            wiki = wiki.replace("</table>", "\n|}")
            markup = markup.replace(table, wiki)
        
        return markup