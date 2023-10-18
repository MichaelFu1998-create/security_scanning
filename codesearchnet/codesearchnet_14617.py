def get_track_by_id(session, track_id, track_point_limit=None, track_point_offset=None):
    """
    Gets a specific track
    """

    tracking_data = {}
    if track_point_limit:
        tracking_data['track_point_limit'] = track_point_limit
    if track_point_offset:
        tracking_data['track_point_offset'] = track_point_offset

    # GET /api/projects/0.1/tracks/{track_id}/

    response = make_get_request(session, 'tracks/{}'.format(track_id),
                                params_data=tracking_data)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['result']
    else:
        raise TrackNotFoundException(message=json_data['message'],
                                     error_code=json_data['error_code'],
                                     request_id=json_data['request_id'])