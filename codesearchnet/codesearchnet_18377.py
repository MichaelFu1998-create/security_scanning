def unusedoptions(self, sections):
        """Lists options that have not been used to format other values in 
        their sections. 
        
        Good for finding out if the user has misspelled any of the options.
        """
        unused = set([])
        for section in _list(sections):
            if not self.has_section(section):
                continue
            options = self.options(section)
            raw_values = [self.get(section, option, raw=True) for option in options]
            for option in options:
                formatter = "%(" + option + ")s"
                for raw_value in raw_values:
                    if formatter in raw_value:
                        break
                else:
                    unused.add(option) 
            return list(unused)