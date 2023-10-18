def download(self, bands, download_dir=None, metadata=False):
        """Download remote .tar.bz file."""
        super(GoogleDownloader, self).validate_bands(bands)
        pattern = re.compile('^[^\s]+_(.+)\.tiff?', re.I)
        image_list = []
        band_list = ['B%i' % (i,) if isinstance(i, int) else i for i in bands]

        if download_dir is None:
            download_dir = DOWNLOAD_DIR

        check_create_folder(join(download_dir, self.sceneInfo.name))
        filename = "%s%s" % (self.sceneInfo.name, self.__remote_file_ext)
        downloaded = self.fetch(self.remote_file_url, download_dir, filename)
        try:

            tar = tarfile.open(downloaded[0], 'r')
            folder_path = join(download_dir, self.sceneInfo.name)
            logger.debug('Starting data extraction in directory ', folder_path)
            tar.extractall(folder_path)
            remove(downloaded[0])
            images_path = listdir(folder_path)

            for image_path in images_path:
                matched = pattern.match(image_path)
                file_path = join(folder_path, image_path)
                if matched and matched.group(1) in band_list:
                    image_list.append([file_path, getsize(file_path)])
                elif matched:
                    remove(file_path)

        except tarfile.ReadError as error:
            logger.error('Error when extracting files: ', error)
            print('Error when extracting files.')

        return image_list