def get_directories(
        self, directory: str = None, packages: typing.List[str] = None
    ) -> typing.List[str]:
        """
        Given `directory` and `packages` arugments, return a list of all the
        directories that should be used for serving static files from.
        """
        directories = []
        if directory is not None:
            directories.append(directory)

        for package in packages or []:
            spec = importlib.util.find_spec(package)
            assert spec is not None, f"Package {package!r} could not be found."
            assert (
                spec.origin is not None
            ), "Directory 'statics' in package {package!r} could not be found."
            directory = os.path.normpath(os.path.join(spec.origin, "..", "statics"))
            assert os.path.isdir(
                directory
            ), "Directory 'statics' in package {package!r} could not be found."
            directories.append(directory)

        return directories