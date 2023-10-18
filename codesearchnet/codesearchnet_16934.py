def _extract_operation_from_view(self, view, args):
        """
        Extract swagger operation details from colander view definitions.

        :param view:
            View to extract information from.
        :param args:
            Arguments from the view decorator.

        :rtype: dict
        :returns: Operation definition.
        """

        op = {
            'responses': {
                'default': {
                    'description': 'UNDOCUMENTED RESPONSE'
                }
            },
        }

        # If 'produces' are not defined in the view, try get from renderers
        renderer = args.get('renderer', '')

        if "json" in renderer:  # allows for "json" or "simplejson"
            produces = ['application/json']
        elif renderer == 'xml':
            produces = ['text/xml']
        else:
            produces = None

        if produces:
            op.setdefault('produces', produces)

        # Get explicit accepted content-types
        consumes = args.get('content_type')

        if consumes is not None:
            # convert to a list, if it's not yet one
            consumes = to_list(consumes)

            # It is possible to add callables for content_type, so we have to
            # to filter those out, since we cannot evaluate those here.
            consumes = [x for x in consumes if not callable(x)]
            op['consumes'] = consumes

        # Get parameters from view schema
        is_colander = self._is_colander_schema(args)
        if is_colander:
            schema = self._extract_transform_colander_schema(args)
            parameters = self.parameters.from_schema(schema)
        else:
            # Bail out for now
            parameters = None
        if parameters:
            op['parameters'] = parameters

        # Get summary from docstring
        if isinstance(view, six.string_types):
            if 'klass' in args:
                ob = args['klass']
                view_ = getattr(ob, view.lower())
                docstring = trim(view_.__doc__)
        else:
            docstring = str(trim(view.__doc__))

        if docstring and self.summary_docstrings:
            op['summary'] = docstring

        # Get response definitions
        if 'response_schemas' in args:
            op['responses'] = self.responses.from_schema_mapping(args['response_schemas'])

        # Get response tags
        if 'tags' in args:
            op['tags'] = args['tags']

        # Get response operationId
        if 'operation_id' in args:
            op['operationId'] = args['operation_id']

        # Get security policies
        if 'api_security' in args:
            op['security'] = args['api_security']

        return op