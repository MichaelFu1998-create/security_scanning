def item_template(self, itemtype):
        """ Get a template for a new item
        """
        # if we have a template and it hasn't been updated since we stored it
        template_name = "item_template_" + itemtype
        query_string = "/items/new?itemType={i}".format(i=itemtype)
        if self.templates.get(template_name) and not self._updated(
            query_string, self.templates[template_name], template_name
        ):
            return copy.deepcopy(self.templates[template_name]["tmplt"])
        # otherwise perform a normal request and cache the response
        retrieved = self._retrieve_data(query_string)
        return self._cache(retrieved, template_name)