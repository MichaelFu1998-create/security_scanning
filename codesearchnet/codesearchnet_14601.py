def create_hireme_project(session, title, description,
                          currency, budget, jobs, hireme_initial_bid):
    """
    Create a fixed project
    """
    jobs.append(create_job_object(id=417))  # Hire Me job, required

    project_data = {'title': title,
                    'description': description,
                    'currency': currency,
                    'budget': budget,
                    'jobs': jobs,
                    'hireme': True,
                    'hireme_initial_bid': hireme_initial_bid
                    }

    # POST /api/projects/0.1/projects/
    response = make_post_request(session, 'projects', json_data=project_data)
    json_data = response.json()
    if response.status_code == 200:
        project_data = json_data['result']
        p = Project(project_data)
        p.url = urljoin(session.url, 'projects/%s' % p.seo_url)
        return p
    else:
        raise ProjectNotCreatedException(message=json_data['message'],
                                         error_code=json_data['error_code'],
                                         request_id=json_data['request_id'],
                                         )