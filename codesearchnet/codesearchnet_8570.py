def get_common_course_modes(self, course_run_ids):
        """
        Find common course modes for a set of course runs.

        This function essentially returns an intersection of types of seats available
        for each course run.

        Arguments:
            course_run_ids(Iterable[str]): Target Course run IDs.

        Returns:
            set: course modes found in all given course runs

        Examples:
            # run1 has prof and audit, run 2 has the same
            get_common_course_modes(['course-v1:run1', 'course-v1:run2'])
            {'prof', 'audit'}

            # run1 has prof and audit, run 2 has only prof
            get_common_course_modes(['course-v1:run1', 'course-v1:run2'])
            {'prof'}

            # run1 has prof and audit, run 2 honor
            get_common_course_modes(['course-v1:run1', 'course-v1:run2'])
            {}

            # run1 has nothing, run2 has prof
            get_common_course_modes(['course-v1:run1', 'course-v1:run2'])
            {}

            # run1 has prof and audit, run 2 prof, run3 has audit
            get_common_course_modes(['course-v1:run1', 'course-v1:run2', 'course-v1:run3'])
            {}

            # run1 has nothing, run 2 prof, run3 has prof
            get_common_course_modes(['course-v1:run1', 'course-v1:run2', 'course-v1:run3'])
            {}

        """
        available_course_modes = None
        for course_run_id in course_run_ids:
            course_run = self.get_course_run(course_run_id) or {}
            course_run_modes = {seat.get('type') for seat in course_run.get('seats', [])}

            if available_course_modes is None:
                available_course_modes = course_run_modes
            else:
                available_course_modes &= course_run_modes

            if not available_course_modes:
                return available_course_modes

        return available_course_modes