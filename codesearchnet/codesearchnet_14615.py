def post_track(session, user_id, project_id, latitude, longitude):
    """
    Start tracking a project by creating a track
    """
    tracking_data = {
        'user_id': user_id,
        'project_id': project_id,
        'track_point': {
            'latitude': latitude,
            'longitude': longitude
        }
    }

    # POST /api/projects/0.1/tracks/
    response = make_post_request(session, 'tracks',
                                 json_data=tracking_data)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['result']
    else:
        raise TrackNotCreatedException(message=json_data['message'],
                                       error_code=json_data['error_code'],
                                       request_id=json_data['request_id'])