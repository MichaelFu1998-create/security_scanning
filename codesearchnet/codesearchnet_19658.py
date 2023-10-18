def parse(src):
    """Note: src should be ascii string"""
    rt = libparser.parse(byref(post), src)
    return (
        rt,
        string_at(post.title, post.tsz),
        string_at(post.tpic, post.tpsz),
        post.body
    )