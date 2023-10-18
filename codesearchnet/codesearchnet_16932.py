def _build_paths(self):
        """
        Build the Swagger "paths" and "tags" attributes from cornice service
        definitions.
        """
        paths = {}
        tags = []

        for service in self.services:
            path, path_obj = self._extract_path_from_service(service)

            service_tags = getattr(service, 'tags', [])
            self._check_tags(service_tags)
            tags = self._get_tags(tags, service_tags)

            for method, view, args in service.definitions:

                if method.lower() in map(str.lower, self.ignore_methods):
                    continue

                op = self._extract_operation_from_view(view, args)

                if any(ctype in op.get('consumes', []) for ctype in self.ignore_ctypes):
                    continue

                # XXX: Swagger doesn't support different schemas for for a same method
                # with different ctypes as cornice. If this happens, you may ignore one
                # content-type from the documentation otherwise we raise an Exception
                # Related to https://github.com/OAI/OpenAPI-Specification/issues/146
                previous_definition = path_obj.get(method.lower())
                if previous_definition:
                    raise CorniceSwaggerException(("Swagger doesn't support multiple "
                                                   "views for a same method. You may "
                                                   "ignore one."))

                # If tag not defined and a default tag is provided
                if 'tags' not in op and self.default_tags:
                    if callable(self.default_tags):
                        op['tags'] = self.default_tags(service, method)
                    else:
                        op['tags'] = self.default_tags

                op_tags = op.get('tags', [])
                self._check_tags(op_tags)

                # Add service tags
                if service_tags:
                    new_tags = service_tags + op_tags
                    op['tags'] = list(OrderedDict.fromkeys(new_tags))

                # Add method tags to root tags
                tags = self._get_tags(tags, op_tags)

                # If operation id is not defined and a default generator is provided
                if 'operationId' not in op and self.default_op_ids:
                    if not callable(self.default_op_ids):
                        raise CorniceSwaggerException('default_op_id should be a callable.')
                    op['operationId'] = self.default_op_ids(service, method)

                # If security options not defined and default is provided
                if 'security' not in op and self.default_security:
                    if callable(self.default_security):
                        op['security'] = self.default_security(service, method)
                    else:
                        op['security'] = self.default_security

                if not isinstance(op.get('security', []), list):
                    raise CorniceSwaggerException('security should be a list or callable')

                path_obj[method.lower()] = op
            paths[path] = path_obj

        return paths, tags