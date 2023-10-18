def _zipped(self, docs_base):
        """ Provide a zipped stream of the docs tree."""
        with pushd(docs_base):
            with tempfile.NamedTemporaryFile(prefix='pythonhosted-', delete=False) as ziphandle:
                pass
            zip_name = shutil.make_archive(ziphandle.name, 'zip')

        notify.info("Uploading {:.1f} MiB from '{}' to '{}'..."
                    .format(os.path.getsize(zip_name) / 1024.0, zip_name, self.target))
        with io.open(zip_name, 'rb') as zipread:
            try:
                yield zipread
            finally:
                os.remove(ziphandle.name)
                os.remove(ziphandle.name + '.zip')