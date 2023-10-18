def create_mss_stream(self, localStreamNames, targetFolder, **kwargs):
        """
        Create a Microsoft Smooth Stream (MSS) out of an existing H.264/AAC
        stream. Smooth Streaming was developed by Microsoft to compete with
        other adaptive streaming technologies.

        :param localStreamNames: The stream(s) that will be used as the input.
            This is a comma-delimited list of active stream names (local
            stream names)
        :type localStreamNames: str

        :param targetFolder: The folder where all the manifest and fragment
            files will be stored. This folder must be accessible by the MSS
            clients. It is usually in the web-root of the server.
        :type targetFolder: str

        :param bandwidths: The corresponding bandwidths for each stream listed
            in `localStreamNames`. Again, this can be a comma-delimited list.
        :type bandwidths: int or str

        :param groupName: The name assigned to the MSS stream or group. If the
            `localStreamNames` parameter contains only one entry and groupName
            is not specified, groupName will have the value of the input
            stream name.
        :type groupName: str

        :param playlistType: Either `appending` or `rolling`
        :type playlistType: str

        :param playlistLength: The number of fragments before the server
            starts to overwrite the older fragments. Used only when
            `playlistType` is `rolling`. Ignored otherwise.
        :type playlistLength: int

        :param manifestName: The manifest file name.
        :type manifestName: str

        :param chunkLength: The length (in seconds) of fragments to be made.
        :type chunkLength: int

        :param chunkOnIDR: If 1 (true), chunking is performed ONLY on IDR.
            Otherwise, chunking is performed whenever chunk length is
            achieved.
        :type chunkOnIDR: int

        :param keepAlive: If 1 (true), the EMS will attempt to reconnect to
            the stream source if the connection is severed.
        :type keepAlive: int

        :param overwriteDestination: If 1 (true), it will allow overwrite of
            destination files.
        :type overwriteDestination: int

        :param staleRetentionCount: How many old files are kept besides the
            ones present in the current version of the playlist. Only
            applicable for rolling playlists.
        :type staleRetentionCount: int

        :param cleanupDestination: If 1 (true), all manifest and fragment
            files in the target folder will be removed before MSS creation is
            started.
        :type cleanupDestination: int

        :param ismType: Either ismc for serving content to client or isml for
            serving content to smooth server.
        :type ismType: int

        :param isLive: If true, creates a live MSS stream, otherwise set to 0
            for VOD.
        :type isLive: int

        :param publishingPoint: This parameter is needed when `ismType=isml`,
            it is the REST URI where the mss contents will be ingested.
        :type publishingPoint: str

        :param ingestMode: Either `single` for a non looping ingest or `loop`
            for looping an ingest.
        :type ingestMode: str

        :link: http://docs.evostream.com/ems_api_definition/createmssstream
        """
        return self.protocol.execute('createmssstream',
                                     localStreamNames=localStreamNames,
                                     targetFolder=targetFolder, **kwargs)