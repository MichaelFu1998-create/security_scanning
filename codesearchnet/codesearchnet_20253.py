def record(self, localStreamName, pathToFile, **kwargs):
        """
        Records any inbound stream. The record command allows users to record
        a stream that may not yet exist. When a new stream is brought into
        the server, it is checked against a list of streams to be recorded.

        Streams can be recorded as FLV files, MPEG-TS files or as MP4 files.

        :param localStreamName: The name of the stream to be used as input
            for recording.
        :type localStreamName: str

        :param pathToFile: Specify path and file name to write to.
        :type pathToFile: str

        :param type: `ts`, `mp4` or `flv`
        :type type: str

        :param overwrite: If false, when a file already exists for the stream
            name, a new file will be created with the next appropriate number
            appended. If 1 (true), files with the same name will be
            overwritten.
        :type overwrite: int

        :param keepAlive: If 1 (true), the server will restart recording every
            time the stream becomes available again.
        :type keepAlive: int

        :param chunkLength: If non-zero the record command will start a new
            recording file after ChunkLength seconds have elapsed.
        :type chunkLength: int

        :param waitForIDR: This is used if the recording is being chunked.
            When true, new files will only be created on IDR boundaries.
        :type waitForIDR: int

        :param winQtCompat: Mandates 32bit header fields to ensure
            compatibility with Windows QuickTime.
        :type winQtCompat: int

        :param dateFolderStructure: If set to 1 (true), folders will be
            created with names in `YYYYMMDD` format. Recorded files will be
            placed inside these folders based on the date they were created.
        :type dateFolderStructure: int

        :link: http://docs.evostream.com/ems_api_definition/record
        """
        return self.protocol.execute('record',
                                     localStreamName=localStreamName,
                                     pathToFile=pathToFile, **kwargs)