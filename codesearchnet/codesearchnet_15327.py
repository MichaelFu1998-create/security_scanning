def exebench(width):
    """
    benchorg.jpg is
    'http://upload.wikimedia.org/wikipedia/commons/d/df/SAND_LUE.jpg'
    """
    height = width * 2 / 3
    with Benchmarker(width=30, loop=N) as bm:
        for i in bm('kaa.imlib2'):
            imlib2_scale('benchorg.jpg', width, height)
        for i in bm("PIL"):
            pil_scale('benchorg.jpg', width, height)
        for i in bm("pgmagick(blob-read)"):
            pgmagick_scale_from_blob('benchorg.jpg', width, height)
        for i in bm("pgmagick(normal-read)"):
            pgmagick_scale('benchorg.jpg', width, height)
        for i in bm("pgmagick(scale+sharpen)"):
            pgmagick_scale_plus_sharpen('benchorg.jpg', width, height)
        for i in bm("opencv"):
            opencv_scale('benchorg.jpg', width, height)
        for i in bm("pyimlib2"):
            pyimlib2_scale('benchorg.jpg', width, height)
        for i in bm("pyimlib2_with_pgsharpen"):
            pyimlib2_scale_with_pgmagicksharpen('benchorg.jpg', width, height)
    return bm.results