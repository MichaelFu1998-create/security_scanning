def create_helpingmaterial(project_id, info, media_url=None, file_path=None):
    """Create a helping material for a given project ID.

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :param info: PYBOSSA Helping Material info JSON field
    :type info: dict
    :param media_url: URL for a media file (image, video or audio)
    :type media_url: string
    :param file_path: File path to the local image, video or sound to upload. 
    :type file_path: string
    :returns: True -- the response status code
    """
    try:
        helping = dict(
            project_id=project_id,
            info=info,
            media_url=None,
        )
        if file_path:
            files = {'file': open(file_path, 'rb')}
            payload = {'project_id': project_id}
            res = _pybossa_req('post', 'helpingmaterial',
                               payload=payload, files=files)
        else:
            res = _pybossa_req('post', 'helpingmaterial', payload=helping)
        if res.get('id'):
            return HelpingMaterial(res)
        else:
            return res
    except:  # pragma: no cover
        raise