def create_project_thread(session, member_ids, project_id, message):
    """
    Create a project thread
    """
    return create_thread(session, member_ids, 'project', project_id, message)