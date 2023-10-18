def translate_array(self, string, language, level=3, retdata=False):
        """Unserializes a serialized php array and prints it to
        the console as a data structure in the specified language.
        Used to translate or convert a php array into a data structure 
        in another language. Currently supports, PHP, Python, Javascript,
        and JSON. 

        Args:
            string: a string of serialized php
        
            language: a string representing the desired output 
            format for the array.

            level: integer, indentation level in spaces. 
            Defaults to 3.

            retdata: boolean, the method will return the string
            in addition to printing it if set to True. Defaults 
            to false.

        Returns:
            None but prints a string to the console if retdata is 
            False, otherwise returns a string.
            """
        language = language.lower()
        assert self.is_built_in(language) or language in self.outer_templates, \
            "Sorry, " + language + " is not a supported language."

        # Serialized data converted to a python data structure (list of tuples)
        data = phpserialize.loads(bytes(string, 'utf-8'), array_hook=list, decode_strings=True)

        # If language conversion is supported by python avoid recursion entirely
        # and use a built in library
        if self.is_built_in(language):
            self.get_built_in(language, level, data) 
            print(self)
            return self.data_structure if retdata else None

        # The language is not supported. Use recursion to build a data structure.
        def loop_print(iterable, level=3):
            """
            Loops over a python representation of a php array 
            (list of tuples) and constructs a representation in another language.
            Translates a php array into another structure.

            Args:
                iterable: list or tuple to unpack.

                level: integer, number of spaces to use for indentation
            """
            retval = ''
            indentation = ' ' * level

            # Base case - variable is not an iterable
            if not self.is_iterable(iterable) or isinstance(iterable, str):
                non_iterable = str(iterable)
                return str(non_iterable)
             
            # Recursive case
            for item in iterable:
                # If item is a tuple it should be a key, value pair
                if isinstance(item, tuple) and len(item) == 2:
                    # Get the key value pair
                    key = item[0]
                    val = loop_print(item[1], level=level+3)
            
                    # Translate special values
                    val = self.translate_val(language, val) if language in self.lang_specific_values \
                          and val in self.lang_specific_values[language] else val
     
                    # Convert keys to their properly formatted strings
                    # Integers are not quoted as array keys
                    key = str(key) if isinstance(key, int) else '\'' + str(key) + '\''

                    # The first item is a key and the second item is an iterable, boolean
                    needs_unpacking = hasattr(item[0],'__iter__') == False \
                                      and hasattr(item[1],'__iter__') == True 

                    # The second item is an iterable
                    if needs_unpacking:
                        retval += self.get_inner_template(language, 'iterable', indentation, key, val)
                    # The second item is not an iterable
                    else:
                        # Convert values to their properly formatted strings
                        # Integers and booleans are not quoted as array values
                        val = str(val) if val.isdigit() or val in self.lang_specific_values[language].values() else '\'' + str(val) + '\''

                        retval += self.get_inner_template(language, 'singular', indentation, key, val) 

            return retval
    
        # Execute the recursive call in language specific wrapper template
        self.data_structure = self.outer_templates[language] % (loop_print(data))
        print(self)
        return self.data_structure if retdata else None