def create_app(
    mapchete_files=None, zoom=None, bounds=None, single_input_file=None,
    mode="continue", debug=None
):
    """Configure and create Flask app."""
    from flask import Flask, render_template_string
    app = Flask(__name__)
    mapchete_processes = {
        os.path.splitext(os.path.basename(mapchete_file))[0]: mapchete.open(
            mapchete_file, zoom=zoom, bounds=bounds,
            single_input_file=single_input_file, mode=mode, with_cache=True,
            debug=debug)
        for mapchete_file in mapchete_files
    }

    mp = next(iter(mapchete_processes.values()))
    pyramid_type = mp.config.process_pyramid.grid
    pyramid_srid = mp.config.process_pyramid.crs.to_epsg()
    process_bounds = ",".join([str(i) for i in mp.config.bounds_at_zoom()])
    grid = "g" if pyramid_srid == 3857 else "WGS84"
    web_pyramid = BufferedTilePyramid(pyramid_type)

    @app.route('/', methods=['GET'])
    def index():
        """Render and hosts the appropriate OpenLayers instance."""
        return render_template_string(
            pkgutil.get_data(
                'mapchete.static', 'index.html').decode("utf-8"),
            srid=pyramid_srid,
            process_bounds=process_bounds,
            is_mercator=(pyramid_srid == 3857),
            process_names=mapchete_processes.keys()
        )

    @app.route(
        "/".join([
            "", "wmts_simple", "1.0.0", "<string:mp_name>", "default",
            grid, "<int:zoom>", "<int:row>", "<int:col>.<string:file_ext>"]),
        methods=['GET'])
    def get(mp_name, zoom, row, col, file_ext):
        """Return processed, empty or error (in pink color) tile."""
        logger.debug(
            "received tile (%s, %s, %s) for process %s", zoom, row, col,
            mp_name)
        # convert zoom, row, col into tile object using web pyramid
        return _tile_response(
            mapchete_processes[mp_name], web_pyramid.tile(zoom, row, col),
            debug)

    return app