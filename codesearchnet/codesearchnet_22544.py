def clear(self, exclude=None):
        """
        Clear build output dir
        :type exclude: list|None
        """
        exclude = exclude or []
        for root, dirs, files in os.walk(self.config.output_dir):
            for f in files:
                if f not in exclude:
                    os.unlink(os.path.join(root, f))
            for d in dirs:
                if d not in exclude:
                    shutil.rmtree(os.path.join(root, d))