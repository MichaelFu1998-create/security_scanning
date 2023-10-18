def supports_file(cls, meta):
        """Check if the loader has a supported file extension"""
        path = Path(meta.path)

        for ext in cls.file_extensions:
            if path.suffixes[:len(ext)] == ext:
                return True

        return False