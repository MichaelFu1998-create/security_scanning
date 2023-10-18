def strip_token(self, text, start, end):
        """{{ a }} -> a"""
        text = text.replace(start, '', 1)
        text = text.replace(end, '', 1)
        return text