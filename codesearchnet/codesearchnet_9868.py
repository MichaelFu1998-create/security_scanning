def iter(self, relations=False, **options):
        """https://github.com/frictionlessdata/datapackage-py#resource
        """

        # Error for non tabular
        if not self.tabular:
            message = 'Methods iter/read are not supported for non tabular data'
            raise exceptions.DataPackageException(message)

        # Get relations
        if relations:
            relations = self.__get_relations()

        return self.__get_table().iter(relations=relations, **options)