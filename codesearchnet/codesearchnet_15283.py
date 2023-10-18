def dropbox_fileupload(dropbox, request):
    """ accepts a single file upload and adds it to the dropbox as attachment"""
    attachment = request.POST['attachment']
    attached = dropbox.add_attachment(attachment)
    return dict(
        files=[dict(
            name=attached,
            type=attachment.type,
        )]
    )