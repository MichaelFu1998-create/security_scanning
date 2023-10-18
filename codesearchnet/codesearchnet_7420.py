def fields_types(self, tname, qstring, itemtype):
        """ Retrieve item fields or creator types
        """
        # check for a valid cached version
        template_name = tname + itemtype
        query_string = qstring.format(i=itemtype)
        if self.templates.get(template_name) and not self._updated(
            query_string, self.templates[template_name], template_name
        ):
            return self.templates[template_name]["tmplt"]
        # otherwise perform a normal request and cache the response
        retrieved = self._retrieve_data(query_string)
        return self._cache(retrieved, template_name)