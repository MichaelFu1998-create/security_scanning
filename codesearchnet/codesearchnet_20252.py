def create_dash_stream(self, localStreamNames, targetFolder, **kwargs):
        """
        Create Dynamic Adaptive Streaming over HTTP (DASH) out of an existing
        H.264/AAC stream. DASH was developed by the Moving Picture Experts
        Group (MPEG) to establish a standard for HTTP adaptive-bitrate
        streaming that would be accepted by multiple vendors and facilitate
        interoperability.

        :param localStreamNames: The stream(s) that will be used as the
            input. This is a comma-delimited list of active stream names
            (local stream names).
        :type localStreamNames: str

        :param targetFolder: The folder where all the manifest and fragment
            files will be stored. This folder must be accessible by the DASH
            clients. It is usually in the web-root of the server.
        :type targetFolder: str

        :param bandwidths: The corresponding bandwidths for each stream listed
            in `localStreamNames`. Again, this can be a comma-delimited list.
        :type bandwidths: int or str

        :param groupName: The name assigned to the DASH stream or group. If
            the `localStreamNames` parameter contains only one entry and
            `groupName` is not specified, `groupName` will have the value of
            the input stream name.
        :type groupName: str

        :param playlistType: Either `appending` or `rolling`.
        :type playlistType: str

        :param playlistLength: The number of fragments before the server
            starts to overwrite the older fragments. Used only when
            `playlistType` is `rolling`. Ignored otherwise.
        :type playlistLength: int

        :param manifestName: The manifest file name.
        :type manifestName: str

        :param chunkLength: The length (in seconds) of fragments to be made.
        :type chunkLength: int

        :param chunkOnIDR: If true, chunking is performed ONLY on IDR.
            Otherwise, chunking is performed whenever chunk length is
            achieved.
        :type chunkOnIDR: int

        :param keepAlive: If true, the EMS will attempt to reconnect to the
            stream source if the connection is severed.
        :type keepAlive: int

        :param overwriteDestination: If true, it will allow overwrite of
            destination files.
        :type overwriteDestination: int

        :param staleRetentionCount: How many old files are kept besides the
            ones present in the current version of the playlist. Only
            applicable for rolling playlists.
        :type staleRetentionCount: int

        :param cleanupDestination: If true, all manifest and fragment files in
            the target folder will be removed before DASH creation is started.
        :type cleanupDestination: int

        :param dynamicProfile: Set this parameter to 1 (default) for a live
            DASH, otherwise set it to 0 for a VOD.
        :type dynamicProfile: int

        :link: http://docs.evostream.com/ems_api_definition/createdashstream
        """
        return self.protocol.execute('createdashstream',
                                     localStreamNames=localStreamNames,
                                     targetFolder=targetFolder, **kwargs)