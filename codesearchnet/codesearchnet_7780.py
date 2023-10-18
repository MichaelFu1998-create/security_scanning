def generate_media_pages(gallery):
    '''Generates and writes the media pages for all media in the gallery'''

    writer = PageWriter(gallery.settings, index_title=gallery.title)

    for album in gallery.albums.values():
        medias = album.medias
        next_medias = medias[1:] + [None]
        previous_medias = [None] + medias[:-1]

        # The media group allows us to easily get next and previous links
        media_groups = zip(medias, next_medias, previous_medias)

        for media_group in media_groups:
            writer.write(album, media_group)