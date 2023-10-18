def delete(self):
        """Remove this resource or collection (recursive).

        See DAVResource.delete()
        """
        if self.provider.readonly:
            raise DAVError(HTTP_FORBIDDEN)
        os.unlink(self._file_path)
        self.remove_all_properties(True)
        self.remove_all_locks(True)