def update_track(session, track_id, latitude, longitude, stop_tracking=False):
    """
    Updates the current location by creating a new track point and appending
    it to the given track
    """

    tracking_data = {
        'track_point': {
            'latitude': latitude,
            'longitude': longitude,
        },
        'stop_tracking': stop_tracking
    }

    # PUT /api/projects/0.1/tracks/{track_id}/

    response = make_put_request(session, 'tracks/{}'.format(track_id),
                                json_data=tracking_data)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['result']
    else:
        raise TrackNotUpdatedException(message=json_data['message'],
                                       error_code=json_data['error_code'],
                                       request_id=json_data['request_id'])