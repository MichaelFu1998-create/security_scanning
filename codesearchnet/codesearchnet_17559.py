def transaction_list(self, start=datetime.min,
                         end=datetime.max,
                         format=ReportFormat.printout,
                         component_path="",
                         output_path=None):
        """
        Generate a transaction list report.

        :param start: The start date to generate the report for.
        :param end: The end date to generate the report for.
        :param format: The format of the report.
        :param component_path: The path of the component to filter the report's
          transactions by.
        :param output_path: The path to the file the report is written to.
          If None, then the report is not written to a file.

        :returns: The generated report.
        """

        rpt = TransactionList(self, start, end, component_path, output_path)
        return rpt.render(format)