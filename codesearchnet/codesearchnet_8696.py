def get_course_runs_from_program(program):
    """
    Return course runs from program data.

    Arguments:
        program(dict): Program data from Course Catalog API

    Returns:
        set: course runs in given program
    """
    course_runs = set()
    for course in program.get("courses", []):
        for run in course.get("course_runs", []):
            if "key" in run and run["key"]:
                course_runs.add(run["key"])

    return course_runs