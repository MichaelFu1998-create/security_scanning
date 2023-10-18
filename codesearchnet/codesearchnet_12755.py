def _get(self, text):
        """
            Analyze the text to get the right function

        Parameters
        ----------
        text : str
            The text that could call a function
        """
        if self.strict:
            match = self.prog.match(text)
            if match:
                cmd = match.group()
                if cmd in self:
                    return cmd
        else:
            words = self.prog.findall(text)
            for word in words:
                if word in self:
                    return word