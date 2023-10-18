def balance_sheet(self, end=datetime.max,
                      format=ReportFormat.printout, output_path=None):
        """
        Generate a transaction list report.

        :param end: The end date to generate the report for.
        :param format: The format of the report.
        :param output_path: The path to the file the report is written to.
          If None, then the report is not written to a file.

        :returns: The generated report.
        """

        rpt = BalanceSheet(self, end, output_path)
        return rpt.render(format)