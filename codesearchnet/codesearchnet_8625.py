def get_course_duration(self, obj):
        """
        Get course's duration as a timedelta.

        Arguments:
            obj (CourseOverview): CourseOverview object

        Returns:
            (timedelta): Duration of a course.
        """
        duration = obj.end - obj.start if obj.start and obj.end else None
        if duration:
            return strfdelta(duration, '{W} weeks {D} days.')
        return ''