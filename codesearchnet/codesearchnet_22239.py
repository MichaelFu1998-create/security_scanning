def skip(course, num=1):
    """
    Go to the next exercise.
    """
    sel = None
    try:
        sel = Exercise.get_selected()
        if sel.course.tid != course.tid:
            sel = None
    except NoExerciseSelected:
        pass

    if sel is None:
        sel = course.exercises.first()
    else:
        try:
            sel = Exercise.get(Exercise.id == sel.id + num)
        except peewee.DoesNotExist:
            print("There are no more exercises in this course.")
            return False

    sel.set_select()
    list_all(single=sel)