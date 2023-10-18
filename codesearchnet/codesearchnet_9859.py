def infer(self, pattern=False):
        """https://github.com/frictionlessdata/datapackage-py#package
        """

        # Files
        if pattern:

            # No base path
            if not self.__base_path:
                message = 'Base path is required for pattern infer'
                raise exceptions.DataPackageException(message)

            # Add resources
            options = {'recursive': True} if '**' in pattern else {}
            for path in glob.glob(os.path.join(self.__base_path, pattern), **options):
                self.add_resource({'path': os.path.relpath(path, self.__base_path)})

        # Resources
        for index, resource in enumerate(self.resources):
            descriptor = resource.infer()
            self.__current_descriptor['resources'][index] = descriptor
            self.__build()

        # Profile
        if self.__next_descriptor['profile'] == config.DEFAULT_DATA_PACKAGE_PROFILE:
            if self.resources and all(map(lambda resource: resource.tabular, self.resources)):
                self.__current_descriptor['profile'] = 'tabular-data-package'
                self.__build()

        return self.__current_descriptor