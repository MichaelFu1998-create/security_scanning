def csv_format(self, row):
        """Converts row values into a csv line
        
        Args:
            row: a list of row cells as unicode
        Returns:
            csv_line (unicode)
        """
        if PY2:
            buf = io.BytesIO()
            csvwriter = csv.writer(buf)
            csvwriter.writerow([c.strip().encode(self.encoding) for c in row])
            csv_line = buf.getvalue().decode(self.encoding).rstrip()
        else:
            buf = io.StringIO()
            csvwriter = csv.writer(buf)
            csvwriter.writerow([c.strip() for c in row])
            csv_line = buf.getvalue().rstrip()
        return csv_line