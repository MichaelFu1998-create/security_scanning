def download(course, tid=None, dl_all=False, force=False, upgradejava=False,
             update=False):
    """
    Download the exercises from the server.
    """

    def dl(id):
        download_exercise(Exercise.get(Exercise.tid == id),
                          force=force,
                          update_java=upgradejava,
                          update=update)

    if dl_all:
        for exercise in list(course.exercises):
            dl(exercise.tid)
    elif tid is not None:
        dl(int(tid))
    else:
        for exercise in list(course.exercises):
            if not exercise.is_completed:
                dl(exercise.tid)
            else:
                exercise.update_downloaded()