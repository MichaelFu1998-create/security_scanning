def post_review(session, review):
    """
    Post a review
    """
    # POST /api/projects/0.1/reviews/
    response = make_post_request(session, 'reviews', json_data=review)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['status']
    else:
        raise ReviewNotPostedException(
            message=json_data['message'],
            error_code=json_data['error_code'],
            request_id=json_data['request_id'])