def infer(self, **options):
        """https://github.com/frictionlessdata/datapackage-py#resource
        """
        descriptor = deepcopy(self.__current_descriptor)

        # Blank -> Stop
        if self.__source_inspection.get('blank'):
            return descriptor

        # Name
        if not descriptor.get('name'):
            descriptor['name'] = self.__source_inspection['name']

        # Only for non inline/storage
        if not self.inline and not self.__storage:

            # Format
            if not descriptor.get('format'):
                descriptor['format'] = self.__source_inspection['format']

            # Mediatype
            if not descriptor.get('mediatype'):
                descriptor['mediatype'] = 'text/%s' % descriptor['format']

            # Encoding
            if not descriptor.get('encoding'):
                contents = b''
                with self.raw_iter(stream=True) as stream:
                    for chunk in stream:
                        contents += chunk
                        if len(contents) > 1000: break
                encoding = cchardet.detect(contents)['encoding']
                if encoding is not None:
                    encoding = encoding.lower()
                    descriptor['encoding'] = 'utf-8' if encoding == 'ascii' else encoding

        # Schema
        if not descriptor.get('schema'):
            if self.tabular:
                descriptor['schema'] = self.__get_table().infer(**options)

        # Profile
        if descriptor.get('profile') == config.DEFAULT_RESOURCE_PROFILE:
            if self.tabular:
                descriptor['profile'] = 'tabular-data-resource'

        # Save descriptor
        self.__current_descriptor = descriptor
        self.__build()

        return descriptor