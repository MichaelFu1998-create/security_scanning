def write_manifest(self):
        """
        Write the manifest content to the zip file. It must be a predictable
        order.
        """
        config = configparser.ConfigParser()

        config.add_section('Manifest')

        for f in sorted(self.manifest.keys()):
            config.set('Manifest', f.replace(
                '\\', '/').lower(), self.manifest[f])

        ini = StringIO()
        config.write(ini)
        self.manifest_data = ini.getvalue()
        self.package_zip.writestr(self.MANIFEST_FILE, self.manifest_data)