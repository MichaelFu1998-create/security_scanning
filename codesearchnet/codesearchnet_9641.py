def write_vector_window(
    in_data=None, out_schema=None, out_tile=None, out_path=None, bucket_resource=None
):
    """
    Write features to GeoJSON file.

    Parameters
    ----------
    in_data : features
    out_schema : dictionary
        output schema for fiona
    out_tile : ``BufferedTile``
        tile used for output extent
    out_path : string
        output path for GeoJSON file
    """
    # Delete existing file.
    try:
        os.remove(out_path)
    except OSError:
        pass

    out_features = []
    for feature in in_data:
        try:
            # clip feature geometry to tile bounding box and append for writing
            # if clipped feature still
            for out_geom in multipart_to_singleparts(
                clean_geometry_type(
                    to_shape(feature["geometry"]).intersection(out_tile.bbox),
                    out_schema["geometry"]
                )
            ):
                out_features.append({
                    "geometry": mapping(out_geom),
                    "properties": feature["properties"]
                })
        except Exception as e:
            logger.warning("failed to prepare geometry for writing: %s", e)
            continue

    # write if there are output features
    if out_features:

        try:
            if out_path.startswith("s3://"):
                # write data to remote file
                with VectorWindowMemoryFile(
                    tile=out_tile,
                    features=out_features,
                    schema=out_schema,
                    driver="GeoJSON"
                ) as memfile:
                    logger.debug((out_tile.id, "upload tile", out_path))
                    bucket_resource.put_object(
                        Key="/".join(out_path.split("/")[3:]),
                        Body=memfile
                    )
            else:
                # write data to local file
                with fiona.open(
                    out_path, 'w', schema=out_schema, driver="GeoJSON",
                    crs=out_tile.crs.to_dict()
                ) as dst:
                    logger.debug((out_tile.id, "write tile", out_path))
                    dst.writerecords(out_features)
        except Exception as e:
            logger.error("error while writing file %s: %s", out_path, e)
            raise

    else:
        logger.debug((out_tile.id, "nothing to write", out_path))