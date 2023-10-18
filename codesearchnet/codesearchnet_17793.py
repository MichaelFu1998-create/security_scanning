def download(self, bands, download_dir=None, metadata=False):
        """Download each specified band and metadata."""
        super(AWSDownloader, self).validate_bands(bands)
        if download_dir is None:
            download_dir = DOWNLOAD_DIR

        dest_dir = check_create_folder(join(download_dir, self.sceneInfo.name))
        downloaded = []

        for band in bands:
            if band == 'BQA':
                filename = '%s_%s.%s' % (self.sceneInfo.name, band, self.__remote_file_ext)
            else:
                filename = '%s_B%s.%s' % (self.sceneInfo.name, band, self.__remote_file_ext)

            band_url = join(self.base_url, filename)
            downloaded.append(self.fetch(band_url, dest_dir, filename))

        if metadata:
            filename = '%s_MTL.txt' % (self.sceneInfo.name)
            url = join(self.base_url, filename)
            self.fetch(url, dest_dir, filename)
        return downloaded