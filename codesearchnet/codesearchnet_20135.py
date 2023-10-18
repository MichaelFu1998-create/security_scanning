def setup(self, *args):
        """Do preparations before printing the first row
        
        Args:
            *args: first row cells 
        """
        self.setup_formatters(*args)
        if self.columns:
            self.print_header()
        elif self.border and not self.csv:
            self.print_line(self.make_horizontal_border())