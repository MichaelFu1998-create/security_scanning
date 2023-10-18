def make_file(self,fromlines,tolines,fromdesc='',todesc='',context=False,
                  numlines=5):
        """Returns HTML file of side by side comparison with change highlights

        Arguments:
        fromlines -- list of "from" lines
        tolines -- list of "to" lines
        fromdesc -- "from" file column header string
        todesc -- "to" file column header string
        context -- set to True for contextual differences (defaults to False
            which shows full differences).
        numlines -- number of context lines.  When context is set True,
            controls number of lines displayed before and after the change.
            When context is False, controls the number of lines to place
            the "next" link anchors before the next change (so click of
            "next" link jumps to just before the change).
        """

        return self._file_template % dict(
            styles = self._styles,
            legend = self._legend,
            table = self.make_table(fromlines,tolines,fromdesc,todesc,
                                    context=context,numlines=numlines))