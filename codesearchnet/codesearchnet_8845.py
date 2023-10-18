def track_enrollment(pathway, user_id, course_run_id, url_path=None):
    """
    Emit a track event for enterprise course enrollment.
    """
    track_event(user_id, 'edx.bi.user.enterprise.onboarding', {
        'pathway': pathway,
        'url_path': url_path,
        'course_run_id': course_run_id,
    })