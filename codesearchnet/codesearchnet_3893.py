def _proc_async_iter_stream(proc, stream, buffersize=1):
    """
    Reads output from a process in a separate thread
    """
    from six.moves import queue
    from threading import Thread
    def enqueue_output(proc, stream, stream_queue):
        while proc.poll() is None:
            line = stream.readline()
            # print('ENQUEUE LIVE {!r} {!r}'.format(stream, line))
            stream_queue.put(line)

        for line in _textio_iterlines(stream):
            # print('ENQUEUE FINAL {!r} {!r}'.format(stream, line))
            stream_queue.put(line)

        # print("STREAM IS DONE {!r}".format(stream))
        stream_queue.put(None)  # signal that the stream is finished
        # stream.close()
    stream_queue = queue.Queue(maxsize=buffersize)
    _thread = Thread(target=enqueue_output, args=(proc, stream, stream_queue))
    _thread.daemon = True  # thread dies with the program
    _thread.start()
    return stream_queue