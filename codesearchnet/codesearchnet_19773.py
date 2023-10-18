def extractFile(self, filename):
        """
        This function will extract a single file from the remote zip without downloading
        the entire zip file. The filename argument should match whatever is in the 'filename'
        key of the tableOfContents.
        """
        files = [x for x in self.tableOfContents if x['filename'] == filename]
        if len(files) == 0:
            raise FileNotFoundException()

        fileRecord = files[0]

        # got here? need to fetch the file size
        metaheadroom = 1024  # should be enough
        request = urllib2.Request(self.zipURI)
        start = fileRecord['filestart']
        end = fileRecord['filestart'] + fileRecord['compressedsize'] + metaheadroom
        request.headers['Range'] = "bytes=%s-%s" % (start, end)
        handle = urllib2.urlopen(request)

        # make sure the response is ranged
        return_range = handle.headers.get('Content-Range')
        if return_range != "bytes %d-%d/%s" % (start, end, self.filesize):
            raise Exception("Ranged requests are not supported for this URI")

        filedata = handle.read()

        # find start of raw file data
        zip_n = unpack("H", filedata[26:28])[0]
        zip_m = unpack("H", filedata[28:30])[0]

        # check compressed size
        has_data_descriptor = bool(unpack("H", filedata[6:8])[0] & 8)
        comp_size = unpack("I", filedata[18:22])[0]
        if comp_size == 0 and has_data_descriptor:
            # assume compressed size in the Central Directory is correct
            comp_size = fileRecord['compressedsize']
        elif comp_size != fileRecord['compressedsize']:
            raise Exception("Something went wrong. Directory and file header disagree of compressed file size")

        raw_zip_data = filedata[30 + zip_n + zip_m: 30 + zip_n + zip_m + comp_size]
        uncompressed_data = ""
        
        # can't decompress if stored without compression
        compression_method = unpack("H", filedata[8:10])[0]
        if compression_method == 0:
          return raw_zip_data

        dec = zlib.decompressobj(-zlib.MAX_WBITS)
        for chunk in raw_zip_data:
            rv = dec.decompress(chunk)
            if rv:
                uncompressed_data = uncompressed_data + rv

        return uncompressed_data