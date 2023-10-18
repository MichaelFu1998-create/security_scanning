def delete(self):
        """Remove this resource or collection (recursive).

        See DAVResource.delete()
        """
        if self.provider.readonly:
            raise DAVError(HTTP_FORBIDDEN)
        shutil.rmtree(self._file_path, ignore_errors=False)
        self.remove_all_properties(True)
        self.remove_all_locks(True)