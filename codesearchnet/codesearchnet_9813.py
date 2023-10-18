def exists_by_source(self):
        """Does this GTFS contain this file? (file specified by the class)"""
        exists_list = []
        for source in self.gtfs_sources:
            if isinstance(source, dict):
                # source can now be either a dict or a zipfile
                if self.fname in source:
                    if source[self.fname]:
                        exists_list.append(True)
                        continue
            # Handle zipfiles specially
            if "zipfile" in source:
                try:
                    Z = zipfile.ZipFile(source['zipfile'], mode='r')
                    Z.getinfo(os.path.join(source['zip_commonprefix'], self.fname))
                    exists_list.append(True)
                    continue
                # File does not exist in the zip archive
                except KeyError:
                    print(self.fname, ' missing in ', source)
                    exists_list.append(False)
                    continue
            # Normal filename
            elif isinstance(source, string_types):
                if os.path.exists(os.path.join(source, self.fname)):
                    exists_list.append(True)
                    continue
            exists_list.append(False)
        # the "file" was not found in any of the sources, return false
        return exists_list