def create_hls_stream(self, localStreamNames, targetFolder, **kwargs):
        """
        Create an HTTP Live Stream (HLS) out of an existing H.264/AAC stream.
        HLS is used to stream live feeds to iOS devices such as iPhones and
        iPads.

        :param localStreamNames: The stream(s) that will be used as the input.
            This is a comma-delimited list of active stream names (local stream
            names).
        :type localStreamNames: str

        :param targetFolder: The folder where all the .ts/.m3u8 files will be
            stored. This folder must be accessible by the HLS clients. It is
            usually in the web-root of the server.
        :type targetFolder: str

        :param keepAlive: If true, the EMS will attempt to reconnect to the
            stream source if the connection is severed.
        :type keepAlive: int

        :param overwriteDestination: If true, it will force overwrite of
            destination files.
        :type overwriteDestination: int

        :param staleRetentionCount: The number of old files kept besides the
            ones listed in the current version of the playlist. Only
            applicable for rolling playlists.
        :type staleRetentionCount: int

        :param createMasterPlaylist: If true, a master playlist will be
            created.
        :type createMasterPlaylist: int

        :param cleanupDestination: If true, all *.ts and *.m3u8 files in the
            target folder will be removed before HLS creation is started.
        :type cleanupDestination: int

        :param bandwidths: The corresponding bandwidths for each stream listed
            in localStreamNames. Again, this can be a comma-delimited list.
        :type bandwidths: int

        :param groupName: The name assigned to the HLS stream or group. If the
            localStreamNames parameter contains only one entry and groupName
            is not specified, groupName will have the value of the input
            stream name.
        :type groupName: str

        :param playlistType: Either appending or rolling.
        :type playlistType: str

        :param playlistLength: The length (number of elements) of the playlist.
            Used only when playlistType is rolling. Ignored otherwise.
        :type playlistLength: int

        :param playlistName: The file name of the playlist (*.m3u8).
        :type playlistName: str

        :param chunkLength: The length (in seconds) of each playlist element
            (*.ts file). Minimum value is 1 (second).
        :type chunkLength: int

        :param maxChunkLength: Maximum length (in seconds) the EMS will allow
            any single chunk to be. This is primarily in the case of
            chunkOnIDR=true where the EMS will wait for the next key-frame. If
            the maxChunkLength is less than chunkLength, the parameter shall
            be ignored.
        :type maxChunkLength: int

        :param chunkBaseName: The base name used to generate the *.ts chunks.
        :type chunkBaseName: str

        :param chunkOnIDR: If true, chunking is performed ONLY on IDR.
            Otherwise, chunking is performed whenever chunk length is
            achieved.
        :type chunkOnIDR: int

        :param drmType: Type of DRM encryption to use. Options are: none
            (no encryption), evo (AES Encryption), SAMPLE-AES (Sample-AES),
            verimatrix (Verimatrix DRM). For Verimatrix DRM, the "drm" section
            of the config.lua file must be active and properly configured.
        :type drmType: str

        :param AESKeyCount: Number of keys that will be automatically generated
            and rotated over while encrypting this HLS stream.
        :type AESKeyCount: int

        :param audioOnly: If true, stream will be audio only.
        :type audioOnly: int

        :param hlsResume: If true, HLS will resume in appending segments to
            previously created child playlist even in cases of EMS shutdown or
            cut off stream source.
        :type hlsResume: int

        :param cleanupOnClose: If true, corresponding hls files to a stream
            will be deleted if the said stream is removed or shut down or
            disconnected.
        :type cleanupOnClose: int

        :param useByteRange: If true, will use the EXT-X-BYTERANGE feature of
            HLS (version 4 and up).
        :type useByteRange: int

        :param fileLength: When using useByteRange=1, this parameter needs to
            be set too. This will be the size of file before chunking it to
            another file, this replace the chunkLength in case of
            EXT-X-BYTERANGE, since chunkLength will be the byte range chunk.
        :type fileLength: int

        :param useSystemTime: If true, uses UTC in playlist time stamp
            otherwise will use the local server time.
        :type useSystemTime: int

        :param offsetTime:
        :type offsetTime: int

        :param startOffset: A parameter valid only for HLS v.6 onwards. This
            will indicate the start offset time (in seconds) for the playback
            of the playlist.
        :type startOffset: int

        :link: http://docs.evostream.com/ems_api_definition/createhlsstream
        """
        return self.protocol.execute('createhlsstream',
                                     localStreamNames=localStreamNames,
                                     targetFolder=targetFolder, **kwargs)