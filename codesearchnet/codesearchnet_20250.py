def create_hds_stream(self, localStreamNames, targetFolder, **kwargs):
        """
        Create an HDS (HTTP Dynamic Streaming) stream out of an existing
        H.264/AAC stream. HDS is used to stream standard MP4 media over
        regular HTTP connections.

        :param localStreamNames: The stream(s) that will be used as the input.
            This is a comma-delimited list of active stream names (local stream
            names).
        :type localStreamNames: str

        :param targetFolder: The folder where all the manifest (*.f4m) and
            fragment (f4v*) files will be stored. This folder must be
            accessible by the HDS clients. It is usually in the web-root of
            the server.
        :type targetFolder: str

        :param bandwidths: The corresponding bandwidths for each stream listed
            in localStreamNames. Again, this can be a comma-delimited list.
        :type bandwidths: int

        :param chunkBaseName: The base name used to generate the fragments.
        :type chunkBaseName: str

        :param chunkLength: The length (in seconds) of fragments to be made.
            Minimum value is 1 (second).
        :type chunkLength: int

        :param chunkOnIDR: If true, chunking is performed ONLY on IDR.
            Otherwise, chunking is performed whenever chunk length is
            achieved.
        :type chunkOnIDR: int

        :param groupName: The name assigned to the HDS stream or group. If the
            localStreamNames parameter contains only one entry and groupName
            is not specified, groupName will have the value of the input
            stream name.
        :type groupName: str

        :param keepAlive: If true, the EMS will attempt to reconnect to the
            stream source if the connection is severed.
        :type keepAlive: int

        :param manifestName: The manifest file name.
        :type manifestName: str

        :param overwriteDestination: If true, it will allow overwrite of
            destination files.
        :type overwriteDestination: int

        :param playlistType: Either appending or rolling.
        :type playlistType: str

        :param playlistLength: The number of fragments before the server
            starts to overwrite the older fragments. Used only when
            playlistType is "rolling". Ignored otherwise.
        :type playlistLength: int

        :param staleRetentionCount: The number of old files kept besides the
            ones listed in the current version of the playlist. Only
            applicable for rolling playlists.
        :type staleRetentionCount: int

        :param createMasterPlaylist: If true, a master playlist will be
            created.
        :type createMasterPlaylist: int

        :param cleanupDestination: If true, all manifest and fragment files in
            the target folder will be removed before HDS creation is started.
        :type cleanupDestination: int

        :link: http://docs.evostream.com/ems_api_definition/createhdsstream
        """
        return self.protocol.execute('createhdsstream',
                                     localStreamNames=localStreamNames,
                                     targetFolder=targetFolder, **kwargs)