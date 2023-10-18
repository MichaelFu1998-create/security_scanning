def case_insensitive_rename(src, dst):
    """A hack to allow us to rename paths in a case-insensitive filesystem like HFS."""
    temp_dir = tempfile.mkdtemp()
    shutil.rmtree(temp_dir)
    shutil.move(src, temp_dir)
    shutil.move(temp_dir, dst)