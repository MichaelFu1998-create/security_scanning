def find_nodes(self, **kwargs):
        """Searches the data nodes that are associated with this graph using
        the key word arguments as a filter and returns a
        :class:`django.db.models.query.QuerySet`` of the attached
        :class:`Node` objects.

        :param kwargs: 
            filter arguments applied to searching the :class:`BaseNodeData`
            subclass associated with this graph.
        :returns: 
            ``QuerySet`` of :class:`Node` objects 
        """
        filter_args = {}
        classname = self.data_content_type.model_class().__name__.lower()
        for key, value in kwargs.items():
            filter_args['%s__%s' % (classname, key)] = value

        return Node.objects.filter(**filter_args)