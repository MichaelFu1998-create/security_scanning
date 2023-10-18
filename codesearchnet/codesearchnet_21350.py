def chunk(self, text, reffs):
        """ Handle a list of references depending on the text identifier using the chunker dictionary.

        :param text: Text object from which comes the references
        :type text: MyCapytains.resources.texts.api.Text
        :param reffs: List of references to transform
        :type reffs: References
        :return: Transformed list of references
        :rtype: [str]
        """
        if str(text.id) in self.chunker:
            return self.chunker[str(text.id)](text, reffs)
        return self.chunker["default"](text, reffs)