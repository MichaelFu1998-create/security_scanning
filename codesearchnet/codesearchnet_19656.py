def get_files_stat(self):
        """get source files' update time"""

        if not exists(Post.src_dir):
            logger.error(SourceDirectoryNotFound.__doc__)
            sys.exit(SourceDirectoryNotFound.exit_code)

        paths = []

        for fn in ls(Post.src_dir):
            if fn.endswith(src_ext):
                paths.append(join(Post.src_dir, fn))

        # config.toml
        if exists(config.filepath):
            paths.append(config.filepath)

        # files: a <filepath to updated time> dict
        files = dict((p, stat(p).st_mtime) for p in paths)
        return files