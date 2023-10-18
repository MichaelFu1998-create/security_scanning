def report(self, format=ReportFormat.printout, output_path=None):
        """
        Returns a report of this class.

        :param format: The format of the report.
        :param output_path: The path to the file the report is written to.
          If None, then the report is not written to a file.

        :returns: The descendants of the account.
        """

        rpt = GlsRpt(self, output_path)
        return rpt.render(format)