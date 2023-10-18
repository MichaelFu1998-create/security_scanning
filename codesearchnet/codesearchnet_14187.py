def convert_pre(self, markup):
        
        """ Substitutes <pre> to Wikipedia markup by adding a space at the start of a line.
        """
        
        for m in re.findall(self.re["preformatted"], markup):
            markup = markup.replace(m, m.replace("\n", "\n "))
            markup = re.sub("<pre.*?>\n{0,}", "", markup)
            markup = re.sub("\W{0,}</pre>", "", markup)
        
        return markup