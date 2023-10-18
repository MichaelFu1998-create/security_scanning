def add_user_jobs(session, job_ids):
    """
    Add a list of jobs to the currently authenticated user
    """
    jobs_data = {
        'jobs[]': job_ids
    }
    response = make_post_request(session, 'self/jobs', json_data=jobs_data)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['status']
    else:
        raise UserJobsNotAddedException(
            message=json_data['message'],
            error_code=json_data['error_code'],
            request_id=json_data['request_id'])