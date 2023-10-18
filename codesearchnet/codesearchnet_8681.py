def send_course_completion_statement(lrs_configuration, user, course_overview, course_grade):
    """
    Send xAPI statement for course completion.

    Arguments:
         lrs_configuration (XAPILRSConfiguration): XAPILRSConfiguration instance where to send statements.
         user (User): Django User object.
         course_overview (CourseOverview): Course over view object containing course details.
         course_grade (CourseGrade): course grade object.
    """
    user_details = LearnerInfoSerializer(user)
    course_details = CourseInfoSerializer(course_overview)

    statement = LearnerCourseCompletionStatement(
        user,
        course_overview,
        user_details.data,
        course_details.data,
        course_grade,
    )
    EnterpriseXAPIClient(lrs_configuration).save_statement(statement)