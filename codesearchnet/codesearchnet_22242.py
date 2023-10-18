def submit(course, tid=None, pastebin=False, review=False):
    """
    Submit the selected exercise to the server.
    """
    if tid is not None:
        return submit_exercise(Exercise.byid(tid),
                               pastebin=pastebin,
                               request_review=review)
    else:
        sel = Exercise.get_selected()
        if not sel:
            raise NoExerciseSelected()
        return submit_exercise(sel, pastebin=pastebin, request_review=review)