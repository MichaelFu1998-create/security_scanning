def get_secrets(prefixes, relative_paths):
    """
    Taken from https://github.com/tokland/youtube-upload/blob/master/youtube_upload/main.py
    Get the first existing filename of relative_path seeking on prefixes directories.
    """
    try:
        return os.path.join(sys._MEIPASS, relative_paths[-1])
    except Exception:
        for prefix in prefixes:
            for relative_path in relative_paths:
                path = os.path.join(prefix, relative_path)
                if os.path.exists(path):
                    return path
        else:
            return None