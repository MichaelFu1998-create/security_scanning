def preview(image, **kwargs):
    ''' Show a slippy map preview of the image. Requires iPython.

    Args:
        image (image): image object to display
        zoom (int): zoom level to intialize the map, default is 16
        center (list): center coordinates to initialize the map, defaults to center of image
        bands (list): bands of image to display, defaults to the image's default RGB bands
    '''
    
    try:
        from IPython.display import Javascript, HTML, display
        from gbdxtools.rda.interface import RDA
        from gbdxtools import Interface
        gbdx = Interface()
    except:
        print("IPython is required to produce maps.")
        return

    zoom = kwargs.get("zoom", 16)
    bands = kwargs.get("bands")
    if bands is None:
        bands = image._rgb_bands
    wgs84_bounds = kwargs.get("bounds", list(loads(image.metadata["image"]["imageBoundsWGS84"]).bounds))
    center = kwargs.get("center", list(shape(image).centroid.bounds[0:2]))
    
    if image.proj != 'EPSG:4326':
        code = image.proj.split(':')[1]
        conn = gbdx.gbdx_connection
        proj_info = conn.get('https://ughlicoordinates.geobigdata.io/ughli/v1/projinfo/{}'.format(code)).json()
        tfm = partial(pyproj.transform, pyproj.Proj(init='EPSG:4326'), pyproj.Proj(init=image.proj))
        bounds = list(ops.transform(tfm, box(*wgs84_bounds)).bounds)
    else:
        proj_info = {}
        bounds = wgs84_bounds
    # Applying DRA to a DRA'ed image looks bad, skip if already in graph
    if not image.options.get('dra'):
        rda = RDA()
        # Need some simple DRA to get the image in range for display.
        dra = rda.HistogramDRA(image)
        image = dra.aoi(bbox=image.bounds)
    graph_id = image.rda_id
    node_id = image.rda.graph()['nodes'][0]['id']
    map_id = "map_{}".format(str(int(time.time())))
    scales = ','.join(['1'] * len(bands))
    offsets = ','.join(['0'] * len(bands))

    display(HTML(Template('''
       <div id="$map_id"/>
       <link href='https://openlayers.org/en/v4.6.4/css/ol.css' rel='stylesheet' />
       <script src="https://cdn.polyfill.io/v2/polyfill.min.js?features=requestAnimationFrame,Element.prototype.classList,URL"></script>
       <style>body{margin:0;padding:0;}#$map_id{position:relative;top:0;bottom:0;width:100%;height:400px;}</style>
       <style></style>
    ''').substitute({"map_id": map_id})))

    js = Template("""
        require.config({
            paths: {
                oljs: 'https://cdnjs.cloudflare.com/ajax/libs/openlayers/4.6.4/ol',
                proj4: 'https://cdnjs.cloudflare.com/ajax/libs/proj4js/2.4.4/proj4'
            }
        });

        require(['oljs', 'proj4'], function(oljs, proj4) {
            oljs.proj.setProj4(proj4)
            var md = $md;
            var georef = $georef;
            var graphId = '$graphId';
            var nodeId = '$nodeId';
            var extents = $bounds;

            var x1 = md.minTileX * md.tileXSize;
            var y1 = ((md.minTileY + md.numYTiles) * md.tileYSize + md.tileYSize);
            var x2 = ((md.minTileX + md.numXTiles) * md.tileXSize + md.tileXSize);
            var y2 = md.minTileY * md.tileYSize;
            var tileLayerResolutions = [georef.scaleX];

            var url = '$url' + '/tile/';
            url += graphId + '/' + nodeId;
            url += "/{x}/{y}.png?token=$token&display_bands=$bands&display_scales=$scales&display_offsets=$offsets";

            var proj = '$proj';
            var projInfo = $projInfo;

            if ( proj !== 'EPSG:4326' ) {
                var proj4def = projInfo["proj4"];
                proj4.defs(proj, proj4def);
                var area = projInfo["area_of_use"];
                var bbox = [area["area_west_bound_lon"], area["area_south_bound_lat"],
                            area["area_east_bound_lon"], area["area_north_bound_lat"]]
                var projection = oljs.proj.get(proj);
                var fromLonLat = oljs.proj.getTransform('EPSG:4326', projection);
                var extent = oljs.extent.applyTransform(
                    [bbox[0], bbox[1], bbox[2], bbox[3]], fromLonLat);
                projection.setExtent(extent);
            } else {
                var projection = oljs.proj.get(proj);
            }

            var rda = new oljs.layer.Tile({
              title: 'RDA',
              opacity: 1,
              extent: extents,
              source: new oljs.source.TileImage({
                      crossOrigin: null,
                      projection: projection,
                      extent: extents,

                      tileGrid: new oljs.tilegrid.TileGrid({
                          extent: extents,
                          origin: [extents[0], extents[3]],
                          resolutions: tileLayerResolutions,
                          tileSize: [md.tileXSize, md.tileYSize],
                      }),
                      tileUrlFunction: function (coordinate) {
                          if (coordinate === null) return undefined;
                          const x = coordinate[1] + md.minTileX;
                          const y = -(coordinate[2] + 1 - md.minTileY);
                          if (x < md.minTileX || x > md.maxTileX) return undefined;
                          if (y < md.minTileY || y > md.maxTileY) return undefined;
                          return url.replace('{x}', x).replace('{y}', y);
                      }
                  })
            });

            var map = new oljs.Map({
              layers: [ rda ],
              target: '$map_id',
              view: new oljs.View({
                projection: projection,
                center: $center,
                zoom: $zoom
              })
            });
        });
    """).substitute({
        "map_id": map_id,
        "proj": image.proj,
        "projInfo": json.dumps(proj_info),
        "graphId": graph_id,
        "bounds": bounds,
        "bands": ",".join(map(str, bands)),
        "nodeId": node_id,
        "md": json.dumps(image.metadata["image"]),
        "georef": json.dumps(image.metadata["georef"]),
        "center": center,
        "zoom": zoom,
        "token": gbdx.gbdx_connection.access_token,
        "scales": scales,
        "offsets": offsets,
        "url": VIRTUAL_RDA_URL
    })
    display(Javascript(js))