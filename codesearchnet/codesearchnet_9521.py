def _process_worker(process, process_tile):
    """Worker function running the process."""
    logger.debug((process_tile.id, "running on %s" % current_process().name))

    # skip execution if overwrite is disabled and tile exists
    if (
        process.config.mode == "continue" and
        process.config.output.tiles_exist(process_tile)
    ):
        logger.debug((process_tile.id, "tile exists, skipping"))
        return ProcessInfo(
            tile=process_tile,
            processed=False,
            process_msg="output already exists",
            written=False,
            write_msg="nothing written"
        )

    # execute on process tile
    else:
        with Timer() as t:
            try:
                output = process.execute(process_tile, raise_nodata=True)
            except MapcheteNodataTile:
                output = None
        processor_message = "processed in %s" % t
        logger.debug((process_tile.id, processor_message))
        writer_info = process.write(process_tile, output)
        return ProcessInfo(
            tile=process_tile,
            processed=True,
            process_msg=processor_message,
            written=writer_info.written,
            write_msg=writer_info.write_msg
        )