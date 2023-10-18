def addattachments(message, template_path):
    """Add the attachments from the message from the commandline options."""
    if 'attachment' not in message:
        return message, 0

    message = make_message_multipart(message)

    attachment_filepaths = message.get_all('attachment', failobj=[])
    template_parent_dir = os.path.dirname(template_path)

    for attachment_filepath in attachment_filepaths:
        attachment_filepath = os.path.expanduser(attachment_filepath.strip())
        if not attachment_filepath:
            continue
        if not os.path.isabs(attachment_filepath):
            # Relative paths are relative to the template's parent directory
            attachment_filepath = os.path.join(template_parent_dir,
                                               attachment_filepath)
        normalized_path = os.path.abspath(attachment_filepath)
        # Check that the attachment exists
        if not os.path.exists(normalized_path):
            print("Error: can't find attachment " + normalized_path)
            sys.exit(1)

        filename = os.path.basename(normalized_path)
        with open(normalized_path, "rb") as attachment:
            part = email.mime.application.MIMEApplication(attachment.read(),
                                                          Name=filename)
        part.add_header('Content-Disposition',
                        'attachment; filename="{}"'.format(filename))
        message.attach(part)
        print(">>> attached {}".format(normalized_path))

    del message['attachment']
    return message, len(attachment_filepaths)