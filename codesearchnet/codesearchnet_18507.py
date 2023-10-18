def get_built_in(self, language, level, data):
        """
        Gets the return string for a language that's supported by python.
        Used in cases when python provides support for the conversion.
    
        Args:
            language: string the langage to return for.

            level: integer, the indentation level.

            data: python data structure being converted (list of tuples)

        Returns:
            None, updates self.data_structure  
        """
        # Language is python
        pp = pprint.PrettyPrinter(indent=level)

        lookup = {'python' : pp.pformat(data),
                  'json' : str(json.dumps(data, sort_keys=True, indent=level, separators=(',', ': ')))}

        self.data_structure = lookup[language]