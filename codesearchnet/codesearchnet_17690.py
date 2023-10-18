def render(self, format=ReportFormat.printout):
        """
        Render the report in the specified format

        :param format: The format. The default format is to print
          the report to the console.

        :returns: If the format was set to 'string' then a string
          representation of the report is returned.
        """

        table = self._generate_table_()
        if format == ReportFormat.printout:
            print(tabulate(table, headers="firstrow", tablefmt="simple"))
        elif format == ReportFormat.latex:
            self._render_latex_(table)
        elif format == ReportFormat.txt:
            self._render_txt_(table)
        elif format == ReportFormat.csv:
            self._render_csv_(table)
        elif format == ReportFormat.string:
            return str(tabulate(table, headers="firstrow", tablefmt="simple"))
        elif format == ReportFormat.matplotlib:
            self._render_matplotlib_()
        elif format == ReportFormat.png:
            if self.output_path is None:
                self._render_matplotlib_()
            else:
                self._render_matplotlib_(True)