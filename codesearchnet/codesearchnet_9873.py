def save(self, target, storage=None, **options):
        """https://github.com/frictionlessdata/datapackage-py#resource
        """

        # Save resource to storage
        if storage is not None:
            if self.tabular:
                self.infer()
                storage.create(target, self.schema.descriptor, force=True)
                storage.write(target, self.iter())

        # Save descriptor to json
        else:
            mode = 'w'
            encoding = 'utf-8'
            if six.PY2:
                mode = 'wb'
                encoding = None
            helpers.ensure_dir(target)
            with io.open(target, mode=mode, encoding=encoding) as file:
                json.dump(self.__current_descriptor, file, indent=4)