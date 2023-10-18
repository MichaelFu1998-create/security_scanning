def operation_upload(uploader, sources, verify, do_compile, do_file, do_restart):
    """The upload operation"""
    sources, destinations = destination_from_source(sources)
    if len(destinations) == len(sources):
        if uploader.prepare():
            for filename, dst in zip(sources, destinations):
                if do_compile:
                    uploader.file_remove(os.path.splitext(dst)[0]+'.lc')
                uploader.write_file(filename, dst, verify)
                #init.lua is not allowed to be compiled
                if do_compile and dst != 'init.lua':
                    uploader.file_compile(dst)
                    uploader.file_remove(dst)
                    if do_file:
                        uploader.file_do(os.path.splitext(dst)[0]+'.lc')
                elif do_file:
                    uploader.file_do(dst)
        else:
            raise Exception('Error preparing nodemcu for reception')
    else:
        raise Exception('You must specify a destination filename for each file you want to upload.')

    if do_restart:
        uploader.node_restart()
    log.info('All done!')