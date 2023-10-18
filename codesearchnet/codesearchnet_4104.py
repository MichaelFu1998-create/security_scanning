def report(self, obj, message, linenum, char_offset=0):
        """Report an error or warning"""
        self.controller.report(linenumber=linenum, filename=obj.path,
                               severity=self.severity, message=message,
                               rulename = self.__class__.__name__,
                               char=char_offset)