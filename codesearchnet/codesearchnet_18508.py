def get_inner_template(self, language, template_type, indentation, key, val):
        """
        Gets the requested template for the given language.

        Args:
            language: string, the language of the template to look for.

            template_type: string, 'iterable' or 'singular'. 
            An iterable template is needed when the value is an iterable
            and needs more unpacking, e.g. list, tuple. A singular template 
            is needed when unpacking is complete and the value is singular, 
            e.g. string, int, float.

            indentation: int, the indentation level.
    
            key: multiple types, the array key.

            val: multiple types, the array values

        Returns:
            string, template formatting for arrays by language.
        """
        #Language specific inner templates
        inner_templates = {'php' : {
                                'iterable' : '%s%s => array \n%s( \n%s%s),\n' % (indentation, key, indentation, val, indentation),
                                'singular' : '%s%s => %s, \n' % (indentation, key, val) },
                           'javascript' : {
                                'iterable' : '%s%s : {\n%s\n%s},\n' % (indentation, key, val, indentation),
                                'singular' : '%s%s: %s,\n' % (indentation, key, val)},
                           'ocaml' : { 
                                'iterable' : '%s[| (%s, (\n%s\n%s))|] ;;\n' % (indentation, key, val, indentation),
                                'singular' : '%s(%s, %s);\n' % (indentation, key, val)}}

        return inner_templates[language][template_type]