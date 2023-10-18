def parse_filename(self, filepath):
        """parse post source files name to datetime object"""
        name = os.path.basename(filepath)[:-src_ext_len]
        try:
            dt = datetime.strptime(name, "%Y-%m-%d-%H-%M")
        except ValueError:
            raise PostNameInvalid
        return {'name': name, 'datetime': dt, 'filepath': filepath}