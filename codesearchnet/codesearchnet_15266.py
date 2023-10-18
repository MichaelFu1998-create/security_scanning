def cleanup(self):
        """ ensures that no data leaks from drop after processing by
        removing all data except the status file"""
        try:
            remove(join(self.fs_path, u'message'))
            remove(join(self.fs_path, 'dirty.zip.pgp'))
        except OSError:
            pass
        shutil.rmtree(join(self.fs_path, u'clean'), ignore_errors=True)
        shutil.rmtree(join(self.fs_path, u'attach'), ignore_errors=True)