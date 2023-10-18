def tcase_comment(tcase):
    """
    Extract testcase comment section / testcase description

    @returns the testcase-comment from the tcase["fpath"] as a list of strings
    """

    src = open(tcase["fpath"]).read()
    if len(src) < 3:
        cij.err("rprtr::tcase_comment: invalid src, tcase: %r" % tcase["name"])
        return None

    ext = os.path.splitext(tcase["fpath"])[-1]
    if ext not in [".sh", ".py"]:
        cij.err("rprtr::tcase_comment: invalid ext: %r, tcase: %r" % (
            ext, tcase["name"]
        ))
        return None

    comment = []
    for line in src.splitlines()[2:]:
        if ext == ".sh" and not line.startswith("#"):
            break
        elif ext == ".py" and not '"""' in line:
            break

        comment.append(line)

    return comment