def get_result(self, course_grade):
        """
        Get result for the statement.

        Arguments:
            course_grade (CourseGrade): Course grade.
        """
        return Result(
            score=Score(
                scaled=course_grade.percent,
                raw=course_grade.percent * 100,
                min=MIN_SCORE,
                max=MAX_SCORE,
            ),
            success=course_grade.passed,
            completion=course_grade.passed
        )