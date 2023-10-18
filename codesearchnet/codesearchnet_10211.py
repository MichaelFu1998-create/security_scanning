def download_files(self, dataset_files, destination='.'):
        """
        Downloads file(s) to a local destination.

        :param dataset_files:
        :type dataset_files: list of :class: `DatasetFile`
        :param destination: The path to the desired local download destination
        :type destination: str
        :param chunk: Whether or not to chunk the file. Default True
        :type chunk: bool
        """
        if not isinstance(dataset_files, list):
            dataset_files = [dataset_files]

        for f in dataset_files:
            filename = f.path.lstrip('/')
            local_path = os.path.join(destination, filename)

            if not os.path.isdir(os.path.dirname(local_path)):
                os.makedirs(os.path.dirname(local_path))

            r = requests.get(f.url, stream=True)

            with open(local_path, 'wb') as output_file:
                shutil.copyfileobj(r.raw, output_file)