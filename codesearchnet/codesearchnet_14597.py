def set_user_jobs(session, job_ids):
    """
    Replace the currently authenticated user's list of jobs with a new list of
    jobs
    """
    jobs_data = {
        'jobs[]': job_ids
    }
    response = make_put_request(session, 'self/jobs', json_data=jobs_data)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['status']
    else:
        raise UserJobsNotSetException(
            message=json_data['message'],
            error_code=json_data['error_code'],
            request_id=json_data['request_id'])