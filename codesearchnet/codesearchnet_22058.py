def process_upload(upload_file, instance, form, event, request):
    """
    Helper function that actually processes and saves the upload(s).
    Segregated out for readability.
    """
    caption = form.cleaned_data.get('caption')
    upload_name = upload_file.name.lower()
    if upload_name.endswith('.jpg') or upload_name.endswith('.jpeg'):
        try:
            upload = Image(
                event=event,
                image=upload_file,
                caption=caption,
            )
            upload.save()
            instance.photos.add(upload)
        except Exception as error:
            messages.error(request, 'Error saving image: {}.'.format(error))