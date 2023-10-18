def progress(length, **kwargs):
    """display a progress that can update in place

    example -- 
        total_length = 1000
        with echo.progress(total_length) as p:
            for x in range(total_length):
                # do something crazy
                p.update(x)

    length -- int -- the total size of what you will be updating progress on
    """
    quiet = False
    progress_class = kwargs.pop("progress_class", Progress)
    kwargs["write_method"] = istdout.info
    kwargs["width"] = kwargs.get("width", globals()["WIDTH"])
    kwargs["length"] = length
    pbar = progress_class(**kwargs)
    pbar.update(0)
    yield pbar
    pbar.update(length)
    br()