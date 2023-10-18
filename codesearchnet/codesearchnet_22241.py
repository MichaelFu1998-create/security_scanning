def select(course=False, tid=None, auto=False):
    """
    Select a course or an exercise.
    """
    if course:
        update(course=True)
        course = None
        try:
            course = Course.get_selected()
        except NoCourseSelected:
            pass

        ret = {}
        if not tid:
            ret = Menu.launch("Select a course",
                              Course.select().execute(),
                              course)
        else:
            ret["item"] = Course.get(Course.tid == tid)
        if "item" in ret:
            ret["item"].set_select()
            update()
            if ret["item"].path == "":
                select_a_path(auto=auto)
            # Selects the first exercise in this course
            skip()
            return
        else:
            print("You can select the course with `tmc select --course`")
            return
    else:
        selected = None
        try:
            selected = Exercise.get_selected()
        except NoExerciseSelected:
            pass

        ret = {}
        if not tid:
            ret = Menu.launch("Select an exercise",
                              Course.get_selected().exercises,
                              selected)
        else:
            ret["item"] = Exercise.byid(tid)
        if "item" in ret:
            ret["item"].set_select()
            print("Selected {}".format(ret["item"]))