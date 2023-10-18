def get_jobs(session, job_ids, seo_details, lang):
    """
    Get a list of jobs
    """
    get_jobs_data = {
        'jobs[]': job_ids,
        'seo_details': seo_details,
        'lang': lang,
    }
    # GET /api/projects/0.1/jobs/
    response = make_get_request(session, 'jobs', params_data=get_jobs_data)
    json_data = response.json()
    if response.status_code == 200:
        return json_data['result']
    else:
        raise JobsNotFoundException(
            message=json_data['message'],
            error_code=json_data['error_code'],
            request_id=json_data['request_id'])