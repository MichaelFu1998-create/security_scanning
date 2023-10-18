def get(self, request, hash, filename):
        """Download a file."""
        if _ws_download is True:
            return HttpResponseForbidden()
        upload = Upload.objects.uploaded().get(hash=hash, name=filename)

        return FileResponse(upload.file, content_type=upload.type)