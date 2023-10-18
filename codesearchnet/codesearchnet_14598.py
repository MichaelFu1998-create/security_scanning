def delete_user_jobs(session, job_ids):
    """
    Remove a list of jobs from the currently authenticated user
    """
    jobs_data = {
        'jobs[]': job_ids
    }
    response = make_delete_request(session, 'self/jobs', json_data=jobs_data)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['status']
    else:
        raise UserJobsNotDeletedException(
            message=json_data['message'],
            error_code=json_data['error_code'],
            request_id=json_data['request_id'])