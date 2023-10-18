def save(self, target=None, storage=None, **options):
        """https://github.com/frictionlessdata/datapackage-py#package
        """

        # Save package to storage
        if storage is not None:
            if not isinstance(storage, Storage):
                storage = Storage.connect(storage, **options)
            buckets = []
            schemas = []
            for resource in self.resources:
                if resource.tabular:
                    resource.infer()
                    buckets.append(_slugify_resource_name(resource.name))
                    schemas.append(resource.schema.descriptor)
            schemas = list(map(_slugify_foreign_key, schemas))
            storage.create(buckets, schemas, force=True)
            for bucket in storage.buckets:
                resource = self.resources[buckets.index(bucket)]
                storage.write(bucket, resource.iter())

        # Save descriptor to json
        elif str(target).endswith('.json'):
            mode = 'w'
            encoding = 'utf-8'
            if six.PY2:
                mode = 'wb'
                encoding = None
            helpers.ensure_dir(target)
            with io.open(target, mode=mode, encoding=encoding) as file:
                json.dump(self.__current_descriptor, file, indent=4)

        # Save package to zip
        else:
            try:
                with zipfile.ZipFile(target, 'w') as z:
                    descriptor = json.loads(json.dumps(self.__current_descriptor))
                    for index, resource in enumerate(self.resources):
                        if not resource.name:
                            continue
                        if not resource.local:
                            continue
                        path = os.path.abspath(resource.source)
                        basename = resource.descriptor.get('name')
                        resource_format = resource.descriptor.get('format')
                        if resource_format:
                            basename = '.'.join([basename, resource_format.lower()])
                        path_inside_dp = os.path.join('data', basename)
                        z.write(path, path_inside_dp)
                        descriptor['resources'][index]['path'] = path_inside_dp
                    z.writestr('datapackage.json', json.dumps(descriptor))
            except (IOError, zipfile.BadZipfile, zipfile.LargeZipFile) as exception:
                six.raise_from(exceptions.DataPackageException(exception), exception)

        return True